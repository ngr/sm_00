from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

#from skill.models import Skill
#from item.models import ItemDirectory

######################################
# MOVE THIS SOMEWHERE FROM TASKS!!!!!!

class Plant(models.Model):
    _name = models.CharField(max_length=127)
    _primary_skill = models.ForeignKey('skill.Skill', related_name='+')
    _secondary_skill   = models.ManyToManyField('skill.Skill', related_name='+')

    _yield_item  = models.ForeignKey('item.ItemDirectory')
    
    _base_yield  = models.PositiveSmallIntegerField(default=1)

    _exec_time   = models.PositiveSmallIntegerField(default=1)

    _plantation_area = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self._name

    def get_primary_skill(self):
        return self._primary_skill

    def get__secondary_skill(self):
        return self._secondary_skill

    def get_yield_item(self):
        return self._yield_item

    def get_base_yield(self):
        return self._base_yield

    def get_exec_time(self):
        return self._exec_time

    def get_plantation_area(self):
        return self._plantation_area



