from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from slave.settings import *
from slave.helpers import *


class ItemManager(models.Manager):
    pass

class ItemDirectory(models.Model):
    """ This is the main list of all types of files. 
        Any subclasses exist here and refer ManyToMany(self) """
    _name    = models.CharField(max_length=127, default='')
    _related   = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self._name

    def get_type(self):
        """ Return list of types relative to ItemType """
        types = {}
        for r in self._related.all():
            for t in ITEM_TYPES:
                if hasattr(r, t[0]):
                    types[t[1]] = r
        return types

    def get_param(self, itype, param):
        """ Return the requested 'param' of 'itype' child """
        if not isinstance(itype, str) or not isinstance(param, str):
            raise TypeError("Attributes should be strings")

        itype = clean_string_title(itype)
        t = [k[0] for k in ITEM_TYPES if k[1] == itype]
        if len(t) == 0:
            raise AttributeError("Invalid attribute 'itype'")

        child_type = getattr(self.get_type()[itype], t[0])
        get_method = getattr(child_type, ('get_' + clean_string_lower(param)))
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

class Item(models.Model):
    _name    = models.CharField(max_length=127, blank=True)
    _itype   = models.ForeignKey(ItemDirectory)
    _amount  = models.PositiveIntegerField(default=1)
    _date_init = models.DateTimeField()
    _building  = models.ForeignKey('area.WarehouseBuilding')

    objects = ItemManager()

    def __str__(self):
        return self._name

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

    def get_amount(self):
        """ Return the amount of items left in pile """
        return self._amount

    def get_type(self):
        return self._itype

    def is_type(self, itype):
        """ Return True if item has properties of itype """
        if not isinstance(itype, str):
            raise TypeError("Requested itype should be string")

        for t in self._itype.get_type().keys():
            if t == clean_string_title(itype):
                return True
        return False


    def get_param(self, param, itype=None, base=True, extra=True):
        """ Return the requested default 'param' with Item instance specific extra """
        if not isinstance(itype, str) or not isinstance(param, str):
            raise TypeError("Attributes should be strings")

        if not hasattr(self, clean_string_lower(itype)):
            raise AttributeError("Item has no properties of itype")

        if base:
            try: 
                base_value = self._itype.get_param(itype, param)
            except AttributeError:
                base_value = None

        if extra:
            try:
                child = getattr(self, clean_string_lower(itype))
                extra_value = child.get_extra(clean_string_lower(param))
            except AttributeError:
                extra_value = None

        if base_value is not None:
            if extra_value is not None:
                if type(base) == type(extra):
                    return base_value + extra_value
                else:
                    raise TypeError("Wrond types in DB")
            else:
                return base_value
        else:
            if extra_value is not None:
                return extra_value
            else:
                raise AttributeError("Item does not have requested param")



class Food(Item):
    _instance_date_expire = models.DateTimeField(null=True) 
    _instance_taste = models.PositiveIntegerField(default=0)
    _instance_satiety = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ' '.join([str(self._itype), str(self._amount)])

    def get_extra(self, param):
        p = '_instance_' + clean_string_lower(param)
        return getattr(self, p)

    def set_expire(self):
        self._date_expire = timezone.now() + datetime.timedelta(seconds=self._itype.get_shelf_life())

#    def __init__(self):
#        self._date_expire = timezone.now() + datetime.timedelta(seconds=self._itype.get_shelf_life())


class Material(Item):
    _density = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ' '.join([str(self._itype), str(self._density)])

