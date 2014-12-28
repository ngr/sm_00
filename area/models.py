from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from operator import itemgetter, attrgetter, methodcaller

#from item.models import Item, Food
from item.models import Item

from slave.helpers import *
from slave.settings import *
#from slave.models import Slave


class RegionManager(models.Manager):
    """ The main interface to operate Regions and locations """



class Region(models.Model):
    name = models.CharField(max_length=127)
    area = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    owner = 1

    objects = RegionManager()

    def get_free_area(self):
        """ Return free area not assigned to locations """
        return self.area - self.location_set.all().aggregate(Sum('area'))['area__sum']

    def get_slaves(self, withdead=True):
        """ List of slaves currently living in HousingDistricts of the Region """
        inhabitants = {}
        districts = self.get_housing()
        for d in districts:
            if withdead:
                inhabitants[d] = d.housingdistrict.get_inhabitants(withdead=True)
            else:
                inhabitants[d] = d.housingdistrict.get_inhabitants()
        print(inhabitants)
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
        return ' '.join([self.name, '-', format(self.area, ',d'), 'm2'])


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

    def set_area(self, a):
        """ Set the area of location if there is free area in Region """
        if not validate_in_range_int(a, MIN_LOCATION_SIZE, super(get_free_area)):
            return False
        self._area = int(float(a))

    def get_type(self):
        """ Returns readable type of location object """
        for t in LOCATION_TYPES:
            if hasattr(self, t[0]):
                return t[1]
        return False
    
    def __str__(self):
        return ' '.join([self.get_name(), '-', format(self._area, ',d'), 'm2'])
    
class FarmingField(Location):
    def get_bonus_yield(self):
        return False

class HousingDistrict(Location):

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

class Warehouse(models.Model):
    _name   = models.CharField(max_length=127, default='Warehouse item')
    _region = models.ForeignKey(Region)
    _item   = models.ForeignKey(Item)

    def __str__(self):
        return self.name


class FoodStock(Warehouse):
    _item = models.ForeignKey(Food)
    
    def put(self, food_type, amount=1, age=0):
        """ Keep in storage the given amount of food.
            If there is food of same type with same expiry age, 
            just add this amount to the pile. """

        ft = FoodType.get(pk=food_type)
#       expiry_date = timezone.now()\
#               + datetime.timedelta(seconds=ft.get_shelf_life())\
#               - datetime.timedelta(seconds=(age * MIN_FOOD_SHELF_LIFE)) * age
#        if ROUND_TO_MINUTES:
#            expiry_date.replace(second=0)
#        expire_date.replace(microsecond=0)

        print("Trying to add % of % to region %s" % (amount, food_type, super(self._region)))
        

    def take(self):
        pass





# Create your models here.
