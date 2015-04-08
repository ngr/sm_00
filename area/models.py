### Area application Models ###
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
#from operator import itemgetter, attrgetter, methodcaller
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
        kwargs['owner'] = owner
        return self.filter(*args, **kwargs)

class Region(models.Model):
    """ Region is the macro element of area distribution. """
    _name = models.CharField(max_length=127)
    _area = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    
    owner = models.ForeignKey('auth.User')

    objects = RegionManager()

    def __str__(self):
        """ Return name of Region. """
        return self._name

    def get_name(self):
        """ Return name of Region. """
        return self._name

    def get_area(self):
        """ Return area of Region. """
        return self._area

    def get_free_area(self):
        """ Return free area not assigned to Locations. """
        return self._area - self.locations.all().aggregate(Sum('_area'))['_area__sum']
    
    def get_owner(self):
        """ Return the current owner of the Region. """
        return self.owner

    def get_locations(self):
        """ Return all Locations of Region. """
        # Foreign key from Location model.
        return self.locations.all()
    
    def get_items(self):
        """ Get Items stored in Region Warehouse. """
        # Foreign key from Warehouse model.
        return self.items.all()
        
    ###############
    # SET methods #
    
    def set_name(self, name=''):
        """ Set a new name of Region. """
        self._name = name

#########        


class BuildingType(models.Model):
    """ This is actually "Location" type. """
    _name       = models.CharField(max_length=127)
    
    def __str__(self):
        return self._name

class BuildingMaterialRecipe(models.Model):
    """ Recipes of materials required to construct buildings. """

    task_type   = models.ForeignKey('task.BuildingTaskDirectory')
    material    = models.ForeignKey('item.MaterialDirectory')
    _amount     = models.PositiveIntegerField(default=1)



class Location(models.Model):
    _name   = models.CharField(max_length=127, blank=True)
    _area    = models.PositiveIntegerField(default=1, validators=[MinValueValidator(MIN_LOCATION_SIZE)])
    _area_used = models.PositiveIntegerField(default=0)
    region  = models.ForeignKey(Region)
    

    def get_name(self):
        """ Return the name of location. """
        return self._name
        
        
    def get_area(self):
        """ Return the area of location. """
        return self._area

    def get_region(self):
        """ Return the parent Region of Location. """
        return self.region
    
    def get_owner(self):
        """ Return the owner of the parent Region. """
        return self.get_region().get_owner()

    def set_area(self, a):
        """ Set the area of location if there is free area in Region """
        if not validate_in_range_int(a, MIN_LOCATION_SIZE, super(get_free_area)):
            return False
        self._area = int(float(a))

    def get_free_area(self):
        """ Returns amount of unused area in Location to determine if Task can be created here. """
        return self._area - self._area_used

    def use_area(self, amount):
        """ Reserves area for some Task. """
        if not amount <= self.get_free_area():
            return False

        self._area_used -= amount
        return True

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
                else self.slave_set.filter(_date_death__isnull=True)

    def get_inhabitants_count(self, withdead=False):
        """ Return current inhabitants of district """
        return self.slave_set.count() if withdead\
                else self.slave_set.filter(_date_death__isnull=True).count()

    def get_free_beds(self):
        """ Return the number of space left for maximum density beds """
        return int(self.get_area() / MIN_BED_AREA - self.get_inhabitants_count())

class Workshop(Location):
    """ This is the Location to craft and build in. """
    
    def get_workers(self):
        """ Get list of Slaves assigned """
        return self.assignment_set.all()
    
    def count_workers(self):
        """ Get number of Slaves assigned to task in this building. """
        return self.assignment_set.all().count()

class Warehouse(models.Model):
    """ Warehouse is a 'Bridge' model for Items, Assignments and Regions.
    Each Item can be located in a single Region. 
    It can be free or used in any Assignments within the Region. """
    
    region = models.ForeignKey(Region, related_name='items')
    item   = models.ForeignKey('item.Item', related_name='warehouse')
    assignment = models.ForeignKey('task.Assignment', related_name='tool', null=True, default=None)

    def __str__(self):
        return ' '.join([str(self.region), 'Warehouse'])

    def get_items(self, itype=None):
        """ Get items optionally filtered by itype. """
        print(" ".join(["itype for area.Warehouse.get_item_list() is:", str(itype)]))
        q = self.objects.all()
        # FIXME! Process strings and validate input.
        if itype:
            q = q.filter(item__itype=itype)
        return q
    
    """
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
    """


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
