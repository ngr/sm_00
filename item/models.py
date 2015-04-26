# ITEM application models # 
#from django.db.models import Q
#from django.core.validators import MaxValueValidator, MinValueValidator
#import operator, functools

import sys
from django.db import models
from django.utils import timezone

from slave.settings import *
from slave.helpers import *

class ItemBaseParam(models.Model):
    """ ManyToMany parameters of ItemDirectory objects. """
    item  = models.ForeignKey('item.ItemDirectory', related_name='params', null=False, blank=False)
    name  = models.ForeignKey('item.ItemParamDirectory', null=False, blank=False)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return '{0} - {1}'.format(self.item, self.name)
    
    class Meta:
        unique_together = (('item', 'name'))

class ItemParamDirectory(models.Model):
    """ Directory of available Item parameters. """
    name = models.CharField(max_length=127, blank=False, unique=True)
    def __str__(self):
        return self.name
        
class ItemDirectory(models.Model):
    """ This is the main list of all types of files. """
    name    = models.CharField(max_length=127, default='', unique=True)

    def __str__(self):
        return self.name

    def get_param(self, param=None):
        """ Return the requested 'param'. """
#        print("Looking for {1} param in ItemDirectory {0}.".format(self, param))
        if isinstance(param, str):
            # Validate that the requested string is OK
            param_q = ItemParamDirectory.objects.filter(name=param)
            if param_q.count() > 0:
                param_key = param_q.all()[0]
            # If some wrong parameter name return a full params list.
            else:
                return self.params.all()
        # In case received an ItemParamDirectory object just use it
        elif isinstance(param, ItemParamDirectory):
            param_key = param
        # If some wrong parameter type or None return a full params list.
        else:
            return self.params.all()
        # Check if param exists for this ItemDirectory object.
        q = self.params.filter(item=self, name=param_key)
        if q.count() > 0:
            return q.all()[0].value 
        else:
            return None

class ItemRecipe(models.Model):
    """ Recipes of materials required to craft items. """
    task_type   = models.ForeignKey('task.CraftingTaskDirectory', unique=True)
    ingredient  = models.ForeignKey(ItemDirectory, related_name='ingredient')
    amount     = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return "{0} ingredient - {1}".format(self.task_type, self.ingredient)
    
class ItemManager(models.Manager):
    def put(self, itype, location, amount=1):
        """ Put amount of items to location. """
        # Check if a record for this type already exists in this location    
        piles = self.filter(location=location, itype=itype).all()
        if piles.count() > 0:
            # Put to this pile
            piles.last().put(amount=amount)
        else:
        # Create a new record (pile)
            pile = Item(itype=itype, location=location, amount=amount, date_init=timezone.now())
            pile.save()

    def take(self, itype, location, amount=sys.maxsize):
        """ Take amount of itype items from location. """
        piles = self.filter(location=location, itype=itype).all()
        # In case we do not have any items of this itype return None.
        if piles.count() == 0:
            return None
        else:
            result = 0
            # Take from piles until we collect requested amount
            for pile in piles.all():
                result += pile.take(amount=amount-result)
                # If we have taken required amount of items return.
                if result == amount:
                    return result
            return result

    def move(self, itype, location, new_location, amount=sys.maxsize):
        """ Move amount of itype items to from location to new_location. """
        # Take the required amount or as much as exists.
        result = self.take(itype=itype, location=location, amount=amount)
        # Put the amount taken to new location
        self.put(itype=itype, location=new_location, amount=result)
        
        # FIXME Connect item specific params!

class Item(models.Model):
    itype   = models.ForeignKey(ItemDirectory)
    amount  = models.PositiveIntegerField(default=1)
    date_init = models.DateTimeField(blank=True, null=True)
    location = models.ForeignKey('area.Location', related_name='items')

    objects = ItemManager()

    def __str__(self):
        return "{0} at {1}: {2}".format(self.itype, self.location, self.amount)

    def get_type(self):
        """ Return ItemDirectory of the Item. """
        return self.itype

    def get_amount(self):
        """ Return the amount of items left in pile """
        return self.amount

    def get_date_init(self):
        return self.date_init

    def get_location(self):
        return self.location

    def is_free(self):
        """ Free Items are stored in HQ only. """
        return str(self.get_location().get_type()) == 'HQ'
    
    def is_food(self):
        """ Is item appropriate to eat. """
        # Food items have param 'food'.
        return str(self.get_type().get_param(param='food')) == '1'
    
    def is_material(self):
        """ Is item appropriate to construct from. """
        # Material items have param 'material'.
        return str(self.get_type().get_param(param='material')) == '1'
        
    def get_param(self, param=None):
        """ Return the requested Item parameter."""
        # No specific item parameters only in directory.
        return self.get_type().get_param(param=None)

#########################################
    def put(self, amount=1):
        """ Increase amount of Item by amount. We assume that all rules are already checked. """
        if not isinstance(amount, int):
            raise TypeError("Amount should be Integer")

        if amount < 0:
            raise AttributeError("Amount should be positive")

        self.amount += amount
        self.save()
        return True


    def take(self, amount=1):
        """ Take the requested (or left) amount of Item and return Integer amount taken """
        if not isinstance(amount, int):
            raise TypeError("Amount should be Integer")

        if amount < 0:
            raise AttributeError("Amount should be positive")

        if self.amount > amount:
            print("Taking {0} of {1}" .format (amount, str(self.itype)))
            self.amount -= amount
            self.save()
            return amount
        else:
            print("Taking only the remaining {0} of {1} from object {2}". \
                format(self.amount, str(self.itype), self.id))
            r = self.amount
            self.delete()
            return r
