# ITEM application models #
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

import operator
import functools

from slave.settings import *
from slave.helpers import *

class ItemParam(models.Model):
    """ ManyToMany parameters of Item objects. """
    item  = models.ForeignKey('item.Item', related_name='params', null=False, blank=False)
    name  = models.ForeignKey('item.ItemParamDirectory', null=False, blank=False)
    value = models.CharField(max_length=255)
    # I decided to try only built-in methods for this directory.
    
    class Meta:
        unique_together = (('item', 'name'))

class ItemBaseParam(models.Model):
    """ ManyToMany parameters of ItemDirectory objects. """
    item  = models.ForeignKey('item.ItemDirectory', related_name='params', null=False, blank=False)
    name  = models.ForeignKey('item.ItemParamDirectory', null=False, blank=False)
    value = models.CharField(max_length=255)
    # I decided to try only built-in methods for this directory.
    
    def __str__(self):
        return '{0} - {1}'.format(self.item, self.name)
    
    class Meta:
        unique_together = (('item', 'name'))

class ItemParamDirectory(models.Model):
    """ Directory of available Item parameters. """
    name = models.CharField(max_length=127, blank=False)
    def __str__(self):
        return self.name
        
class ItemDirectory(models.Model):
    """ This is the main list of all types of files. """
    name    = models.CharField(max_length=127, default='')

    def __str__(self):
        return self.name

    def get_param(self, param=None):
        """ Return the requested 'param'. """
        print("Looking for {1} param {0} in ItemDirectory.".format(self, param))
        if not isinstance(param, str):
            return self.params
        print(self.params)
        return self.params.get(item=self, name=param).value

class ItemRecipe(models.Model):
    """ Recipes of materials required to craft items. """
    task_type   = models.ForeignKey('task.CraftingTaskDirectory')
    ingredient  = models.ForeignKey(ItemDirectory, related_name='ingredient')
    amount     = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return "{0} ingredient - {1}".format(self.task_type, self.ingredient)
    
class ItemManager(models.Manager):
    pass
    
class Item(models.Model):
    itype   = models.ForeignKey(ItemDirectory)
    amount  = models.PositiveIntegerField(default=1)
    date_init = models.DateTimeField()
    location = models.ForeignKey('area.Location', related_name='items')

    objects = ItemManager()

    def __str__(self):
        return self.name

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
        print(self.get_location().get_type())
        return self.get_location().get_type() == 'HQ'

    def get_param(self, param):
        """ Return the requested ItemDirectory parameter."""
        if not isinstance(param, str):
            raise TypeError("Attributes should be strings")
        print("Looking for {1} param of instance {0}".format(self, param))

     # Get base parameter for this ItemType
        try: 
            item_param_value = self.get_type().get_param(param=param)
        except AttributeError:
            item_param_value = None
#        print("Base:", item_param_value)
    # Check for any Item-specific parameters
        try: 
            item_param_value += self.params.get(item=self, name=param).value
        except AttributeError:
            pass # We have already initialized item_param_value to None
       
        return item_param_value

        
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
            print("Taking % of %" % (amount, str(self.itype)))
            self.amount -= amount
            self.save()
            return amount
        else:
            print("Taking only the remaining {0} of {1} from object {2}". \
                format(self.amount, str(self.itype), self.id))
            r = self.amount
            self.delete()
            return r
