import datetime

from django.db import models
from django.utils import timezone

class Slave(models.Model):

    MALE = 1
    FEMALE = 0

    BLUE = 0
    CYAN = 1
    AQUA = 2

    SEX_CHOICES = (
            (MALE, 'Male'),
            (FEMALE, 'Female'),
            )
    RACE_CHOICES = (
            (BLUE, 'Blue'),
            (CYAN, 'Cyan'),
            (AQUA, 'Aqua'),
            )
    name = models.CharField(max_length=127)
    date_init = models.DateTimeField('date initialised')
    sex = models.IntegerField(choices=SEX_CHOICES, default=MALE)
    race = models.IntegerField(choices=RACE_CHOICES, default=BLUE)
    happiness = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def is_child(self):
        return timezone.now() - datetime.timedelta(days=10) <= self.date_init <= timezone.now()

class SlaveAttributes(models.Model):
    sid = models.ForeignKey(Slave, unique=True)
    intelligence = models.PositiveSmallIntegerField(default=1)
    strength = models.PositiveSmallIntegerField(default=1)
    agility = models.PositiveSmallIntegerField(default=1)
    charisma = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.sid.name

# Create your models here.
