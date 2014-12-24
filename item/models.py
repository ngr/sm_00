from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from slave.settings import *



class ItemManager(models.Manager):
    pass


class ItemType(models.Model):
    """ Types of items with common properties """
    name    = models.CharField(max_length=127, default='')
    
    def __str__(self):
        return self.name

class ItemDirectory(models.Model):
    """ Do not worry that this 3-step schema looks complicated. Will be OK """
    name    = models.CharField(max_length=127, default='')
    itype   = models.ForeignKey(ItemType)

    def __str__(self):
        return ' - '.join([str(self.itype), self.name])


class Item(models.Model):
    itype   = models.ForeignKey(ItemDirectory)

    objects = ItemManager()

    def __str__(self):
        return self.itype

    def put(self):
        pass

    def take(self):
        pass

    def destroy(self):
        pass


""" class FoodDirectory(ItemDirectory):
    _taste   = models.PositiveSmallIntegerField(default=1)
    _shelf_life = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

    def get_taste(self):
        return self._taste

    def get_shelf_life(self):
        return self._shelf_life

    #### ADD SOME VALIDATION HERE ###
    def set_taste(self, taste=1):
        pass

    def set_shelf_life(self, time=MIN_FOOD_SHELF_LIFE):
        pass """



class Food(Item):
#    _itype   = models.ForeignKey(FoodDirectory)
    _amount  = models.PositiveIntegerField(default=0)
    _date_expire = models.DateTimeField() 
    # I decide to calculate expire on init, not on check age

    def __str__(self):
        return ' '.join([str(self._itype), str(self._amount)])

    def get_amount(self):
        """ Return the amount of food left in pile """
        return self._amount

    def take(self, amount=1):
        """ Take the requested (or left) amount of food and return Integer amount taken """
        if not isinstance(amount, Integer):
            raise TypeError("Amount should be Integer")

        if amount < 0:
            raise AttributeError("Amount should be positive")

        if self._amount > amount:
 #           print("Taking % of %" % (amount, self._itype))
            self.amount -= amount
            self.save()
            return amount
        else:
#            print("Taking only the remaining % of %" % (self.amount, self._itype))
            r = self.amount
            self.amount = 0
            self.save()
            return r

    def put(self, amount=1):
        """ Increase amount of food by amount. We assume that age and type is already checked. """
        if not isinstance(amount, Integer):
            raise TypeError("Amount should be Integer")

        if amount < 0:
            raise AttributeError("Amount should be positive")

        self.amount += amount
        self.save()
        return True



