from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from skill.models import Skill

class Plant(models.Model):
    name = models.CharField(max_length=127)
    primary_skill = models.ForeignKey(Skill, related_name='+')
    secondary_skill   = models.ManyToManyField(Skill, related_name='+')

    base_yield  = models.PositiveSmallIntegerField(default=1,\
        validators=[MinValueValidator(0), MaxValueValidator(100)])

    exec_time   = models.PositiveSmallIntegerField(default=1,\
        validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name


