import datetime
from random import random, randrange, choice
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage

""" HERE ARE SOME HELPERS """
def random_line(afile):
    """ Returns a random line from given afile """
    line = next(afile)
    for num, aline in enumerate(afile):
        if randrange(num + 2): continue
        line = aline
    return line


class SlaveManager(models.Manager):

    def spawn(self, **kwargs):
        larva = self.create(date_birth=timezone.now())
        MIN_ATTR = 1
        MAX_ATTR = 10
        DELTA_ATTR = 2

    # Define larva race
        if 'race' in kwargs:
            larva.race = kwargs['race']
        else:
            larva.race = choice([0,1,2])
        print("Race is set to:", larva.race)
    
    # Define attributes 
    # Default values are overwritten by hard set in kwargs
    # Defaults are randomized with DELTA_ATTR
        defaults = RaceDefaults.objects.all().filter(race=larva.race)
        for param in defaults:
            if param.param in kwargs:
                val = kwargs.pop(param.param)
            else:
                val = sorted([MIN_ATTR, (param.value + randrange(-DELTA_ATTR, DELTA_ATTR)), MAX_ATTR])[1]
            print("Optimal val", param.param, "=", val)
            setattr(larva, param.param, val)
    # Now setting rest of hard set in kwargs
        for param, value in kwargs.items():
            setattr(larva, param, value)
            print("Hard param:", param, "=", value)
    # Setting sex if not yet defined
        if not larva.sex:
            larva.sex = choice([0, 1])

    # Setting name if not yet defined
        if not larva.name:
            print("Try to choose name")
            larva.name = self.generate_name(larva.sex, larva.race)
        print("Name:", larva.name)

        larva.save()
        return larva

    def generate_name(self, sex, race):
        path = FileSystemStorage(location='slave/etc')
        dict_name = 'names_'
        #sex = choice([0, 1]) if sex is None else sex
        dict_name += 'male_' if sex == 0 else 'female_'
        dict_name += (str(race)+'.txt')
        file_with_names = open('/'.join([path.location, dict_name]), 'r')
        return random_line(file_with_names)

class RaceDefaults(models.Model):
    race = models.CharField(max_length=15)
    param = models.CharField(max_length=127)
    value = models.SmallIntegerField(default=0,\
            validators=[MinValueValidator(-100), MaxValueValidator(100)])

    def __str__(self):
        return ' '.join([self.race, self.param])

class Slave(models.Model):

    MALE = True
    FEMALE = False

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
    date_birth = models.DateTimeField('Date of birth')
    date_death = models.DateTimeField('Date of death', null=True)
    sex = models.BooleanField(choices=SEX_CHOICES, default=None )
    race = models.PositiveSmallIntegerField(choices=RACE_CHOICES, default=BLUE)

    intelligence = models.PositiveSmallIntegerField(default=1,\
            validators=[MinValueValidator(1), MaxValueValidator(10)])
    strength = models.PositiveSmallIntegerField(default=1,\
            validators=[MinValueValidator(1), MaxValueValidator(10)])
    agility = models.PositiveSmallIntegerField(default=1,\
            validators=[MinValueValidator(1), MaxValueValidator(10)])
    charisma = models.PositiveSmallIntegerField(default=1,\
            validators=[MinValueValidator(1), MaxValueValidator(10)])

    happiness = models.SmallIntegerField(default=0,\
            validators=[MinValueValidator(-100), MaxValueValidator(100)])
    satiety = models.PositiveSmallIntegerField(default=0,\
            validators=[MinValueValidator(0), MaxValueValidator(100)])

    objects = SlaveManager()

    def __str__(self):
        return self.name

    def is_child(self):
        return timezone.now() - datetime.timedelta(days=10) <= self.date_birth <= timezone.now()

    def is_adult(self):
        return self.date_birth + datetime.timedelta(days=10) <= timezone.now() and not self.date_death

    def is_alive(self):
        return self.date_birth <= timezone.now() and not self.date_death

    


