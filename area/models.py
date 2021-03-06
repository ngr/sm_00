### Area application Models ###

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
#from operator import itemgetter, attrgetter, methodcaller
import datetime

#from item.models import Item

from slave.helpers import *
from slave.settings import *
from slave.logic import AreaError

class Region(models.Model):
    """ Region is the macro element of area distribution. """
    name = models.CharField(max_length=127)
    area = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    
    owner = models.ForeignKey('auth.User')

#    objects = RegionManager()

    def __str__(self):
        """ Return name of Region. """
        return self.name

    def get_name(self):
        """ Return name of Region. """
        return self.name

    def get_area(self):
        """ Return area of Region. """
        return self.area

    def get_free_area(self):
        """ Return free area not assigned to Locations. """
        return self.area - self.locations.all().aggregate(Sum('design__area'))['design__area__sum']
    
    def get_owner(self):
        """ Return the current owner of the Region. """
        return self.owner 

    def get_locations(self, ltype=None, design=None):
        """ Return Locations of Region. """
    ## Check the ltype of requested attribute
        if isinstance(ltype, LocationType):
            location_type = ltype
        elif isinstance(ltype, int):
            location_type = LocationType.objects.get(pk=ltype)
        elif isinstance(ltype, str):
            location_type = LocationType.objects.filter(name=ltype).first()
        else:
            location_type = None
            
    ## Check the design of requested attribute
        if isinstance(design, LocationDirectory):
            location_design = design
        elif isinstance(design, int):
            location_design = LocationDirectory.objects.get(pk=design)
        elif isinstance(design, str):
            location_design = LocationDirectory.objects.filter(name=design).first()
        else:
            location_design = None
        
    ## Make the resulting Queryset
        q = self.locations.all()
        if location_type:
            q = q.filter(design__type=location_type).all()
        if location_design:
            q = q.filter(design=location_design).all()

    ## Return filtered or clear set of Region Locations.
        return q
    
    def get_items(self):
        """ Get Items stored in Region Warehouse. """
        # Foreign key from Warehouse model.
        return self.items.all()
        
    ###############
    # SET methods #
    # FIXME Use this for debugging only now!
    def set_name(self, name=''):
        """ Set a new name of Region. """
        self.name = name
        
    def set_owner(self, owner):
        """ Change owner of Region. """
        self.owner = owner

class LocationType(models.Model):
    """ This is General type of Locations. """
    name        = models.CharField(max_length=127)
    
    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

class LocationDirectory(models.Model):
    """ This is Location design directory. """
    name        = models.CharField(max_length=127)
    area        = models.PositiveIntegerField(default=1)
    type        = models.ForeignKey('area.LocationType')
    
    def __str__(self):
        return self.name

    def get_name(self):
        """ Return name of LocationDirectory. """
        return self.name
        
    def get_type(self):
        """ Global type of this LocationDirectory. """
        return self.type

    def get_area(self):
        """ Default Area of this LocationDirectory. """
        return self.area

class BuildingMaterialRecipe(models.Model):
    """ Recipes of materials required to construct Locations. """
    task_type   = models.ForeignKey('task.BuildingTaskDirectory', related_name='materials')
    ingredient  = models.ForeignKey('item.ItemDirectory', related_name='building_recipes')
    amount      = models.PositiveIntegerField(default=1)
    def __str__(self):
        """ Return the name of Recipe. """
        return "{0} for {1} recipe".format(self.ingredient, self.task_type)

        
class Location(models.Model):
    name   = models.CharField(max_length=127, blank=True)
    region  = models.ForeignKey(Region, related_name='locations')
    design  = models.ForeignKey(LocationDirectory)

    def __str__(self):
        """ Return the name of location. """
        return "{0} - {1} ".format(self.name, self.get_design())

    def get_name(self):
        """ Return the name of location. """
        return self.name
        
    def get_area(self):
        """ Return the area of location. """
        return self.get_design().get_area()

    def get_region(self):
        """ Return the parent Region of Location. """
        return self.region

    def get_design(self):
        """ Return the LocationDesign. """
        return self.design

    def get_type(self):
        """ Return the LocationDirectory General Type. """
        return self.get_design().get_type()
    
    def get_owner(self):
        """ Return the owner of the parent Region. """
        return self.get_region().get_owner()

    def get_tasks(self, running=True):
        """ List of current tasks in Location. """
        return self.tasks.filter(_retrieved=False, _fulfilled__lt=100.0).all()\
            if running else self.tasks.all()
        
    def get_free_area(self):
        """ Returns amount of unused area in Location to determine if Task can be created here. """
        # FIXME!
        # Get all Tasks in Location
        tasks = self.get_tasks(running=True)
        # Get area used by each task
        area_used_by_tasks = [t.get_assignments(running=True).count() \
                * t.get_type().get_area_per_worker() for t in tasks]
        return self.get_area() - sum(area_used_by_tasks)

    def get_items(self):
        """ List of Items in Location. """
        return self.items
