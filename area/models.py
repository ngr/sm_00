from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from operator import itemgetter, attrgetter, methodcaller
import datetime

from item.models import Item

from slave.helpers import *
from slave.settings import *
#from slave.models import Slave


class RegionManager(models.Manager):
    """ The main interface to operate Regions and locations """

    def auth_get_region(self, owner, region=None):
        """ Return region or all regions of 'owner' """
        args = ()
        kwargs = {}

        if region:
            kwargs['pk'] = region

# This should be the last param
        kwargs['_owner'] = owner
        return self.filter(*args, **kwargs)



class Region(models.Model):
    _name = models.CharField(max_length=127)
    area = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    _owner = models.ForeignKey('auth.User')

    objects = RegionManager()

    def get_free_area(self):
        """ Return free area not assigned to locations """
        return self.area - self.location_set.all().aggregate(Sum('area'))['area__sum']

    def get_owner(self):
        """ Return the current owner of the Region """
        return self._owner

    def auth_allowed(self, user):
        """ Check permissions to access object """
        return self.get_owner() == user

    def get_slaves(self, withdead=False, free=False, by_districts=False):
        """ List of slaves currently living in HousingDistricts of the Region """
        inhabitants = {}
        districts = self.get_housing()
        for d in districts:
            if withdead:
                inhabitants[d] = d.housingdistrict.get_inhabitants(withdead=True)
            else:
                inhabitants[d] = d.housingdistrict.get_inhabitants()
#        print(inhabitants)

        if by_districts:
            for k, v in inhabitants.items():
                inhabitants[k] = [s for s in v if s.is_free()]
            
        else:
            temp = []
            for k, v in inhabitants.items():
                temp += v
#            print(temp)
            inhabitants = temp
            if free:
                inhabitants = [s for s in inhabitants if s.is_free()]      
        return inhabitants
     
#    def get_slaves_count(self, withdead=False):
#        """ List of slaves currently located in Region """
#        return self.slave_set.all().filter(date_death__isnull=True).count() if not withdead\
#            else self.slave_set.all().count()

    def get_housing(self, district=False):
        """ Show housing statistics for Region. """
        locations = self.location_set.all()
#       print(locations)
        districts = {}
        for l in locations:
            if hasattr(l, 'housingdistrict'):
                districts[l] = {}
                districts[l]['area'] = l.get_area()
                districts[l]['comfort'] = l.housingdistrict.get_comfort()
                districts[l]['inhabitants'] = l.housingdistrict.get_inhabitants_count()
                districts[l]['free'] = l.housingdistrict.get_free_beds()
#        print(districts)
        return districts

    def get_farming_areas(self):
        """ Show farming statistics for Region """
    # We may want to make universal function for different types of locations
        locations = self.location_set.all()
        districts = {}
        for l in locations:
            if hasattr(l, 'farmingfield'):
                districts[l] = {}
                districts[l]['area'] = l.get_area()
        return districts


    def house_slave(self, slave):
        housing = self.get_housing()

        housing = sorted(housing.items(), key=lambda k_v: k_v[1]['comfort'], reverse=True)
# There should be multiple sort keys or smth. Ticket #13
#        housing = sorted(housing, key=lambda k_v: k_v[1]['free'], reverse=True)

        if len(housing) == 0 or housing[0][1]['free'] == 0:
            print("No housing available in Region!")
            return False
        else:
            print("Housing in %s with comfort %s. Inhabs %s, free %s" % (housing[0][0].housingdistrict, housing[0][1]['comfort'], housing[0][1]['beds'], housing[0][1]['free']))
            return housing[0][0].housingdistrict

        print(housing)
#        if housing[0][0].housingdistrict.add_inhabitant():
#            print("Successfully housed slave")
#            return housing[0][0].housingdistrict 
#        else:
#            print("Could not add inhabitant to ", housing[0])

    def get_locations(self):
        """ Return all locations of region """
        return self.location_set.all()

    def __str__(self):
        return self._name


    def put_to_warehouse(self, item, amount=1):
        """ This is the main entry function to put items to Region warehouses """
        wh = self.warehouse_set.last()
        wh.put(item, amount)
#        print("Putting {2} of {1} to warehouse {3} in region {0}".format(self, item, amount, wh))

    def get_item_list(self, itype=None):
        """ Return items from region warehouses """
        # Accumulate info to result
        result = []
        # Get items from each Warehouse
        for warehouse in self.warehouse_set.all():
            print(warehouse)
            new_item = warehouse.get_item_list(itype)
        # Function can return a single object or a list
            print(type(new_item))
            if isinstance(new_item, (list, tuple)):
                result.extend(new_item)
            elif isinstance(new_item, Item):
                result.append(new_item)

        # FIXME process result to accumulate similar items from different warehouses
        # return processed result
        print(result)
        return result



class Location(models.Model):
    _name   = models.CharField(max_length=127, blank=True)
    _area    = models.PositiveIntegerField(default=1, validators=[MinValueValidator(MIN_LOCATION_SIZE)])
    region  = models.ForeignKey(Region)

    def get_name(self):
        """ Return the name of location """
        return self._name
        
        
    def get_area(self):
        """ Return the area of location """
        return self._area

    def get_region(self):
        """ Return the parent Region of Location """
        return self.region

    def set_area(self, a):
        """ Set the area of location if there is free area in Region """
        if not validate_in_range_int(a, MIN_LOCATION_SIZE, super(get_free_area)):
            return False
        self._area = int(float(a))

    def get_type(self):
        """ Returns readable type of location object """
        for t in LOCATION_TYPES:
            if hasattr(self, t[0]):
                return t[0]
        return False

    def get_type_str(self):
        """ Returns readable type of location object """
        for t in LOCATION_TYPES:
            if hasattr(self, t[0]):
                return t[1]
        return False
    
    def __str__(self):
        return ' '.join([self.get_name(), '-', format(self._area, ',d'), 'm2'])
    
class FarmingField(Location):
    """ Farming tasks are performed in this Locations. """
    _area_used = models.PositiveIntegerField(default=0)

    def get_free_area(self):
        """ Returns amount of unused area in Location to determine if Task can be created here. """
        return self._area - self._area_used

    def use_area(self, amount):
        """ Reserves area for some Task. """
        if not amount <= self.get_free_area():
            return False

        self._area_used -= amount
        return True

    def get_bonus_yield(self):
        """ This to be done later """
        return False

class HousingDistrict(Location):
    """ Required living area for Slaves. Actually represents a building. """

#    def add_inhabitant(self, number=1):
#        """ Add 'number' of new inhabitants to housing district if fit """
#        if not validate_in_range_int(number, 1, (self.area / MIN_BED_AREA - self.get_beds())):
#            print("Over limit for beds")
#            return False
#        else:
#            return True

    def get_comfort(self):
        """ Should return more complex comfort later """
        max_guys, min_guys = self.get_area() / MIN_BED_AREA, self.get_area() / MAX_BED_AREA
        c = -(self.get_inhabitants_count() /(max_guys - min_guys)) + max_guys / (max_guys - min_guys)
        return 1 if c > 1 else c

    def get_inhabitants(self, withdead=False):
        """ Return current inhabitants of district """
        return self.slave_set if withdead\
                else self.slave_set.filter(date_death__isnull=True)

    def get_inhabitants_count(self, withdead=False):
        """ Return current inhabitants of district """
        return self.slave_set.count() if withdead\
                else self.slave_set.filter(date_death__isnull=True).count()

    def get_free_beds(self):
        """ Return the number of space left for maximum density beds """
        return int(self.get_area() / MIN_BED_AREA - self.get_inhabitants_count())




##############
# Warehouses #
##############

#class WHM(models.Manager):
    
#    def get_warehouse(self, region, whtype=None):
#        wh = self.all().filter(_building___region=region).all()
#        return wh


class Warehouse(models.Model):
#    _name   = models.CharField(max_length=127)
    _region = models.ForeignKey(Region)
#    _name   = models.CharField(max_length=127, choices=ITEM_TYPES)

# One day we shall add limit of storage available in Warehouse

    def __str__(self):
        return ' '.join([str(self._region), 'Warehouse'])

#    def get_type(self):
#        return self._type

#    class Meta:
#        unique_together = (('_region', '_type'))

    def get_item_list(self, itype):
#        print(" ".join(["itype for area.Warehouse.get_item_list() is:", str(itype)]))
        return list(Item.objects.get_items_of_type(itype=itype, warehouse=self))



        #return self.item_set.objects.get_items_of_type(itype=itype, warehouse=self)

    def put(self, item, amount=1):
        print("Putting {2} of {1} to the warehouse {0}".format(self, item, amount))
        
        try:
            i = Item.objects.get(_itype=item, _date_init=next_game_period(GAME_MONTH))
        except:
            i=None
        if i:
            print("Found {0}".format(i))
            i.put(amount)
        else:
            print("Not found valid instance of {0}. Creating a new one.".format(item))
            i = Item(_name=str(item), 
                    _itype=item, 
                    _amount=amount, 
                    _date_init=next_game_period(GAME_MONTH),
                    _warehouse=self)
            i.save()



#class Warehouse(models.Model):
#    name  = models.CharField(max_length=127)

    #    _building = models.ForeignKey(WarehouseBuilding)
#    _item   = models.ForeignKey(Item, unique=True)

#    objects = WHM()

#    def __str__(self):
#        return str(self._item)



#    name  = models.CharField(max_length=127)

#    def __init__(self):
#        super(Warehouse, self)._item = models.ForeignKey(Food)

    
#    def put(self, food_type, amount=1, age=0):
#        """ Keep in storage the given amount of food.
#            If there is food of same type with same expiry age, 
#            just add this amount to the pile. """

#        ft = FoodType.get(pk=food_type)
#       expiry_date = timezone.now()\
#               + datetime.timedelta(seconds=ft.get_shelf_life())\
#               - datetime.timedelta(seconds=(age * MIN_FOOD_SHELF_LIFE)) * age
#        if ROUND_TO_MINUTES:
#            expiry_date.replace(second=0)
#        expire_date.replace(microsecond=0)
#
#        print("Trying to add {0} of {1} to FoodStock of region {2}".format(amount, food_type, super(self._region)))
        
#
#    def take(self):
#        pass


# Create your models here.
