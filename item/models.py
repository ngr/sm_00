# ITEM application models #
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

import operator
import functools

from slave.settings import *
from slave.helpers import *


class ItemDirectory(models.Model):
    """ This is the main list of all types of files. 
        Any subclasses exist here and refer ManyToMany(self) """
    _name    = models.CharField(max_length=127, default='')
    _related   = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self._name

    def get_related(self):
        return self._related.all()

    def get_child_types(self):
        """ Return list of types relative to ItemType """
        types = {}
        for r in self._related.all():
            for t in ITEM_TYPES:
                if hasattr(r, t[0]):
                    types[t[1]] = r
        return types

    def get_param(self, itype, param):
        """ Return the requested 'param' of 'itype' child """
#        print("Looking for {1} param {0} in ItemDirectory instance {2}".format(param, itype, self))
        if not isinstance(itype, str) or not isinstance(param, str):
            raise TypeError("Attributes for ItemDirectory.get_param() should be strings")
 
        itype = clean_string_title(itype)
        t = [k[0] for k in ITEM_TYPES if k[1] == itype]
        if len(t) == 0:
            raise AttributeError("Invalid attribute 'itype'")

        child_type = getattr(self.get_child_types()[itype], t[0])
        get_method = getattr(child_type, ('get_' + clean_string_lower(param)))
#        print("We use method: {0}".format(get_method))
        return get_method()

    def is_core(self):
        if self._related.all().count() > 0:
            return True
        else:
            return False
    is_core.admin_order_field = '_related'
    is_core.boolean = True
    is_core.short_description = "Core Item"

class MaterialDirectory(ItemDirectory):
    _density = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return ' '.join(['Material', self._name])

    def get_density(self):
        return self._density

class FoodDirectory(ItemDirectory):
    _taste   = models.PositiveSmallIntegerField(default=1)
    _satiety = models.PositiveSmallIntegerField(default=1)
    _shelf_life = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return ' '.join(['Food', self._name])

    def get_taste(self):
        return self._taste

    def get_satiety(self):
        return self._satiety

    def get_shelf_life(self):
        return self._shelf_life

    #### ADD SOME VALIDATION HERE ###
    def set_taste(self, taste=1):
        pass

    def set_satiety(self, val=1):
        pass

    def set_shelf_life(self, time=MIN_FOOD_SHELF_LIFE):
        pass

class ItemRecipe(models.Model):
    """ Recipes of materials required to craft items. """
    task_type   = models.ForeignKey('task.CraftingTaskDirectory', related_name='task_type')
    ingredient  = models.ForeignKey(ItemDirectory, related_name='ingredient')
    _amount     = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return "{0} ingredient - {1}".format(self.task_type, self.ingredient)
    
class ItemManager(models.Manager):
    def get_items_of_type(self, itype=None, warehouse=None):
        """ Return objects of type/types from warehouse.
            itype can be a string (name of item), an ItemDirectory object,
            or tuple/list of these mixed the way you like. 
            If building is not specified return all of type. """
        kwargs = {}   # Query filter Dict
        args = []      # Query filter Q_objects here 

        if itype is not None:
            if isinstance(itype, (list, tuple)):
#               print("Received multiple types", itype)
                tmp = [Q(_itype=i) for i in itype if isinstance(i, ItemDirectory)]
                tmp += [Q(_itype___name=i) for i in itype if isinstance(i,str)]
#                   print("TMP Q:", tmp)
                args.append(functools.reduce(operator.or_, tmp))

            elif isinstance(itype, ItemDirectory):
#                print("Received a single ItemDirectory object")
                kwargs['_itype'] = itype
            elif isinstance(itype, str):
#                print("Received a single string")
                kwargs['_itype___name'] = itype.strip()
            else:
                raise AttributeError("Invalid itypes for get_items_of_type()")

# FIXME! Need to check validity of building here
        if warehouse:
            kwargs['warehouse'] = warehouse

        if not args and not kwargs:
            raise AttributeError("Valid itype or warehouse is required for get_items_of_type().")

        print(self.filter(*args, **kwargs))
        return self.filter(*args, **kwargs)

class Item(models.Model):
    _name    = models.CharField(max_length=127, blank=True)
    _itype   = models.ForeignKey(ItemDirectory)
    _amount  = models.PositiveIntegerField(default=1)
    _date_init = models.DateTimeField()
#    warehouse = models.ForeignKey('area.Warehouse', related_name='item')
    # This is done with other way ForeignKey

    objects = ItemManager()

    def __str__(self):
        return self._name

    def get_type(self):
        return self._itype

    def get_amount(self):
        """ Return the amount of items left in pile """
        return self._amount

    def get_date_init(self):
        return self._date_init

    def get_warehouse(self):
        return self.warehouse

#########################################
    def put(self, amount=1):
        """ Increase amount of Item by amount. We assume that all rules are already checked. """
        if not isinstance(amount, int):
            raise TypeError("Amount should be Integer")

        if amount < 0:
            raise AttributeError("Amount should be positive")

        self._amount += amount
        self.save()
        return True


    def take(self, amount=1):
        """ Take the requested (or left) amount of Item and return Integer amount taken """
        if not isinstance(amount, int):
            raise TypeError("Amount should be Integer")

        if amount < 0:
            raise AttributeError("Amount should be positive")

        if self._amount > amount:
            print("Taking % of %" % (amount, str(self._itype)))
            self._amount -= amount
            self.save()
            return amount
        else:
            print("Taking only the remaining % of %" % (self.amount, str(self._itype)))
            r = self.amount
            self.amount = 0
            self.save()
            return r

    def destroy(self):
        pass


    def is_type(self, itype):
        """ Return True if item has properties of itype """
        if not isinstance(itype, str):
            raise TypeError("Requested itype should be string")

        for t in self._itype.get_type().keys():
            if t == clean_string_title(itype):
                return True
        return False


    def get_param(self, param, itype=None, base=True):
        """ Return the requested default 'param' with Item instance specific extra """
        if not isinstance(itype, str)  and not isinstance(param, str):
            raise TypeError("Attributes should be strings")
#        print("Looking for {0} param {1} of instance {2}".format(itype, param, self))

        if base:
            try: 
                base_value = self.get_type().get_param(itype, param)
            except AttributeError:
                base_value = None
#        print("Base:", base_value)

        if base_value is not None:
            return base_value
        else:
            raise AttributeError("Item does not have requested param")


class ItemJoffreyList(models.Model):
    """ This is a queue for execution of items for any automatic reasons (expiration) """
    item        = models.ForeignKey(Item, unique=True)
    execution_time   = models.DateTimeField()
    reason      = models.CharField(max_length=255, blank=True)
