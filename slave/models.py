import datetime
from random import random, randrange, choice
from math import floor
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage
from slave.settings import *

from skill.models import Skill, SkillTrained
from area.models import HousingDistrict
from task.models import Assignment

""" HERE ARE SOME HELPERS """
def random_line(afile):
    """ Returns a random line from given afile """
    line = next(afile)
    for num, aline in enumerate(afile):
        if randrange(num + 2): continue
        line = aline
    return line


class SlaveManager(models.Manager):

    APP_ROOT_PATH = '/var/django/sm_00/slave'

    def spawn(self, **kwargs):
        larva = self.create(date_birth=timezone.now())
        MIN_ATTR = 1
        MAX_ATTR = 10
        DELTA_ATTR = 2
        VALID_ATTRIBS = ['intelligence', 'strength', 'agility',\
                    'charisma', 'name', 'date_birth', 'date_death',\
                     'race', 'sex', 'happiness', 'satiety']

    # Define larva race
        if 'race' in kwargs:
            larva.race = kwargs['race']
        else:
            larva.race = choice([0,1,2])
#        print("Race is set to:", larva.race)
    
    # Define attributes 
    # Default values are overwritten by hard set in kwargs
    # Defaults are randomized with DELTA_ATTR
        defaults = RaceDefaults.objects.all().filter(race=larva.race)
        for param in defaults:
            if param.param in kwargs:
                val = kwargs.pop(param.param)
            else:
                val = sorted([MIN_ATTR, (param.value + randrange(-DELTA_ATTR, DELTA_ATTR)), MAX_ATTR])[1]
#            print("Optimal val", param.param, "=", val)
            setattr(larva, param.param, val)
    # Now setting rest of hard set in kwargs
        for param, value in kwargs.items():
            if param not in VALID_ATTRIBS: 
                continue
            setattr(larva, param, value)
#            print("Hard defined param:", param, "=", value)

    # Setting sex if not yet defined
        if larva.sex is None:
            larva.sex = choice([0, 1])

    # Setting name if not yet defined
        if not larva.name:
 #           print("Try to choose name")
            larva.name = self.__generate_name(larva.sex, larva.race)
#        print("Name:", larva.name)

        larva.save()
       
    # If parents are setin kwargs, make connections
        if 'parents' in kwargs:
            parents = kwargs['parents']
            ps = Parents(larva.id)
            ps.save()
            ps.child.add(larva.id)
            if isinstance(parents, int):
#                print("One parent specified:", parents)
                ps.parent.add(parents)
            elif isinstance(parents, tuple):
#                print("Multiple parents specified:", parents)
                if len(parents) > 2:
                    raise AttributeError("Only 2 parents allowed")
                for p in parents:
                    ps.parent.add(p)

        return larva

    def kill(self, victim, dd=None):
        """ Kills the victim. May specify date. """
        if not dd:
            dd = timezone.now()
#        print("Killing", victim, victim.id)

# Filter() is commented as it seems to be less productive than get->set->save
#       Slave.objects.filter(pk=victim.id).update(date_death=dd)
        try:
            sl = Slave.objects.get(pk=victim.id)
            sl.date_death = dd
            sl.save()
        except Model.DoesNotExist:
            print("Killing failed")
            return False

    def __generate_name(self, sex, race):
        """ Helper to take some random slave name """
        path = FileSystemStorage(location='/'.join([__class__.APP_ROOT_PATH, 'etc']))
        dict_name = 'names_'
        dict_name += 'male_' if sex == 1 else 'female_'
        dict_name += (str(race)+'.txt')
        file_with_names = open('/'.join([path.location, dict_name]), 'r')
        return random_line(file_with_names).rstrip()


class Slave(models.Model):

#    MALE = True
#    FEMALE = False

#    GAME_YEAR = 3600
#    BABY_AGE = 5
#    CHILD_AGE = 15
#    REPRODUCTIVE_AGE = 25
    
#    BLUE = 0
#    CYAN = 1
#    AQUA = 2

#    SEX_CHOICES = (
#            (MALE, 'Male'),
#            (FEMALE, 'Female'),
#            )
#    RACE_CHOICES = (
#            (BLUE, 'Blue'),
#            (CYAN, 'Cyan'),

#            (AQUA, 'Aqua'),
#            )
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

    location = models.ForeignKey(HousingDistrict, null=True)

    objects = SlaveManager()

    def __str__(self):
        return self.name

    def get_name(self):
        """ Return the name of the Slave """
        return self.name

    def get_age(self):
        """ Return age of the Slave """
        return floor((timezone.now() - self.date_birth).total_seconds() / GAME_YEAR)

    def is_baby(self):
        return timezone.now() - datetime.timedelta(seconds=(GAME_YEAR * BABY_AGE))\
            <= self.date_birth <= timezone.now() and not self.date_death

    def is_child(self):
        return self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * BABY_AGE))\
            <= timezone.now()\
            <= self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * CHILD_AGE))\
            and not self.date_death
    
    def is_reproductive(self):
        return self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * CHILD_AGE))\
            <= timezone.now()\
            <= self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * REPRODUCTIVE_AGE))\
            and not self.date_death

    def is_adult(self):
        return self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * CHILD_AGE))\
                <= timezone.now() and not self.date_death

    def is_alive(self):
        return self.date_birth <= timezone.now() and not self.date_death

#    def get_skills(self, *args):
    """ Returns the current skill level on requested skills.
            Args can be a list or single skills.
            If skill is not trained return 0 value.
            If args not set return all skills. """
#        result = {}

#        if not args:
    """ Returning all trained skills.
            Should one day take all skills and return zeros if not trained
            same as we do it if request exists. """
#            sk_all = self.skilltrained_set.all()
#            sk_all = SkillTrained.objects.get_available_skills(self)
#            print(sk_all)
#            if len(sk_all) > 0:
#                for s in sk_all:
#                    result[s] = SkillTrained.objects.get_skill_level(self, s)
#            return result

#        for sk in args:
#            print("Requested slave skill:", self, sk)

    """print("sk is Skill instance:", sk.__class__.__name__ == 'Skill')
            if sk.__class__.__name__ == 'Skill':
                if self.skilltrained_set.filter(skill=sk).exists():
                    result[sk] = self.skilltrained_set.get(skill=sk).level
                else:
                    result[sk] = 0
            else:
                for s in sk:
#                    print("Processing s:", s)
                    if self.skilltrained_set.filter(skill=s).exists():
#                       print("Looks like this skill is trained:", s)
                       result[s] = self.skilltrained_set.get(skill=s).level
                    else:
                        result[s] = 0"""


    """if self.skilltrained_set.filter(skill=sk).exists():
                    if sk.all().count() > 1: # Any of args can be a list
                        for s in sk.all():
                            if self.skilltrained_set.filter(skill=s).exists():
#                               print("Looks like this secondary skill is trained:", s)
                                result[s] = self.skilltrained_set.get(skill=s).level
                    else:
                # We know that skilltrained is unique so use get()
                        result[sk] = self.skilltrained_set.get(skill=sk).level
                else:
                    result[sk] = 0 """
#       print("Returning:", result)
#        return result


    def get_skill(self, skill):
        return SkillTrained.objects.get_skill_level(self, skill)

    def get_available_skills(self):
        return SkillTrained.objects.get_available_skills(self)

    def get_trained_skills(self):
        result = {}
        sk_all = SkillTrained.objects.get_available_skills(self)
        if len(sk_all) > 0:
            for s in sk_all:
                result[s] = SkillTrained.objects.get_skill_level(self, s)
        return result


########################
# Slave update
    def set_skill(self, skill, exp):
        """ This is an admin function. Should hide it later. """
        print(skill,exp)
        sk = Skill.objects.get(pk=skill)
        SkillTrained.objects.set_st(self, sk, exp)

    def set_location(self, region):
        """ House the slave to the given region """
        try:
            loc = region.house_slave(self)
        except:
            print("Could not house %s to region %s" % (self, region))
            return False

        if loc:
            self.location = loc
            self.save()







#################################
#################################
class RaceDefaults(models.Model):
    race = models.CharField(max_length=15)
    param = models.CharField(max_length=127)
    value = models.SmallIntegerField(default=0,\
            validators=[MinValueValidator(-100), MaxValueValidator(100)])

    def __str__(self):
        return ' '.join([self.race, self.param])


    
class Parents(models.Model):
    """ This model keeps track of parent relationships. """ 
    child = models.ManyToManyField(Slave)
    parent = models.ManyToManyField(Slave, related_name='parent')

