### SLAVE application models ###

import datetime
from random import random, randrange, choice
#from math import floor
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from slave.settings import *
from slave.helpers import *

from area.models import Location
from skill.models import Skill, SkillTrained
from task.models import Assignment, Task, TaskDirectory as TD

class SlaveManager(models.Manager):

    APP_ROOT_PATH = '/var/django/sm_00/slave'

    def auth_get_slave(self, owner, slave=None, withdead=False):
        """ Return slave or all slaves of 'owner' """
        args = ()
        kwargs = {}

        if slave:
            kwargs['pk'] = slave

        if not withdead:
            kwargs['_date_death__isnull'] = True


        # This should be the last param for security reasons
        kwargs['owner'] = owner
        return self.filter(*args, **kwargs)

    def spawn(self, **kwargs):
        """ Spawn a new slave with random parameters but you can force any in kwargs. """
        larva = self.create(date_birth=timezone.now())
        MIN_ATTR = 1
        MAX_ATTR = 10
        DELTA_ATTR = 2
        VALID_ATTRIBS = ['intelligence', 'strength', 'agility',\
                    'charisma', 'name', 'date_birth', 'date_death',\
                     'race', 'sex', 'happiness', 'satiety', 'owner', 'location']

    # Define larva race
        if 'race' in kwargs:
            larva.race = kwargs['race']
        else:
        # FIXME! Need to use setting here to choose race
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
                print("BAD PARAM", param)
                continue
            # FIXME Try to use ints without fetching User and Location
            # Get Owner if specified int
            if param == 'owner' and isinstance(value, int):
                value = User.objects.get(pk=value)
            # Get Location if specified int
            if param == 'location' and isinstance(value, int):
                value = Location.objects.get(pk=value)

            # Finally try to set attribute. As this is service
            # function we do not manage exceptions for now.
            setattr(larva, param, value)
#            print("Hard defined param:", param, "=", value)

    # Setting sex if not yet defined
        if larva.sex is None:
            larva.sex = choice(['m', 'f'])

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

    """       
    def kill(self, victim, dd=None):
        "" Kills the victim. May specify date. ""
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
    """
    def __generate_name(self, sex, race):
        """ Helper to take some random slave name """
        path = FileSystemStorage(location='/'.join([__class__.APP_ROOT_PATH, 'etc']))
        dict_name = 'names_'
        dict_name += 'male_' if sex == 1 else 'female_'
        dict_name += (str(race)+'.txt')
        file_with_names = open('/'.join([path.location, dict_name]), 'r')
        return random_line(file_with_names).rstrip()

class Slave(models.Model):
    """ This is the main unit in the game. """
    name = models.CharField(max_length=127)
    date_birth = models.DateTimeField('Date of birth')
    date_death = models.DateTimeField('Date of death', null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
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

    location = models.ForeignKey('area.Location', null=True, blank=True)
    owner   = models.ForeignKey('auth.User', related_name='slaves', default=1)

    objects = SlaveManager()

    def __str__(self):
        """ Return the name of the Slave """
        return self.name

    def get_name(self):
        """ Return the name of the Slave """
        return self.name

# AGE SECTION
    def is_baby(self):
        """ Return if Slave is in 'baby' age period. """
        return timezone.now() - datetime.timedelta(seconds=(GAME_YEAR * BABY_AGE))\
            <= self.date_birth <= timezone.now() and not self.date_death

    def is_child(self):
        """ Return if Slave is in 'child' age period. """
        return self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * BABY_AGE))\
            <= timezone.now()\
            <= self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * CHILD_AGE))\
            and not self.date_death
    
    def is_reproductive(self):
        """ Return if Slave is in 'reproductive' age period. """
        return self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * CHILD_AGE))\
            <= timezone.now()\
            <= self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * REPRODUCTIVE_AGE))\
            and not self.date_death

    def is_adult(self):
        """ Return if Slave is in 'adult' age period. """
        return self.date_birth + datetime.timedelta(seconds=(GAME_YEAR * CHILD_AGE))\
                <= timezone.now() and not self.date_death

    def is_alive(self):
        """ Return if Slave is already born and not yet dead. """
        return self.date_birth <= timezone.now() and not self.date_death

    def get_age(self):
        """ Return current age of Slave or age when he died (in game years). """
        if self.date_death is not None:
            return int((self.date_death - self.date_birth).total_seconds() // GAME_YEAR)
        else:
            return int((timezone.now() - self.date_birth).total_seconds() // GAME_YEAR)

    def get_location(self):
        """ Return current location of Slave """
        return self.location

    def get_region(self):
        """ Return current Region of Slave """
        return self.location.get_region()

    def get_owner(self):
        """ Return the current owner of the Slave """
        return self.owner

#    def auth_allowed(self, user):
#        """ Check if user is owner. More complex access rights to be developed. """
#        return self.get_owner() == user

# ATTRIBUTES SECTION
    from slave.settings import ATTRIBUTE_CHOICES
    
    def get_attribute(self, attribute):
        """ Return the current value of Slave attribute. Attribute must be string. """
        # Check validity of type
        if not isinstance(attribute, str):
            print("Invalid type for Slave->get_attribute. Must be name of attribute in string.")
            return False

        # If requested string check if it works
        # FIXME Need to check here! Now accepts only full names of parameters.
        attr_name = clean_string_lower(attribute)
            
        # Finally get and return attribute value.
        try:
            return getattr(self, attr_name)
        except:
        # Getting is not critical to False is returned
            print("Invalid attribute name for Slave->get_attribute(). Must be name of attribute.")
            return False
            
    """    
    def set_attribute(self, attribute, value):
        "" Set new value to Slave attribute. ""
        # This is critical to set exact attribute so full name required here.
        if not isinstance(attribute, str):
            raise AttributeError("Wrong input type for Slave->set_attribute()")
        
        # Now check if attribute is a correct name of attribute
        attr_name = clean_string_lower(attribute)
        if not any(attribute.title() in names for names in ATTRIBUTE_CHOICES):
            raise AttributeError("Wrong attribute name for Slave->set_attribute()")
            
        # Check if value is in correct range
        if not validate_in_range_int(value, minv=1, maxv=10):
            raise AttributeError("Wrong value for attribute in Slave->set_attribute()")

        # Now we try to change the attribute
        try:
            setattr(self, ''.join(['_', clean_string_lower(attribute)]), value)
        except:
        # This is critical to set exact attribute.
            raise AttributeError("Wrong input for set_attribute()")
        
        # Save attribute changes to DB
        self.save()
        return self.get_attribute(attribute) """

# SKILLS SECTION
    def get_skills(self):
        """ Get a list of already trained skills. """
        return self.skills

    def get_total_exp(self):
        """ Return accumulated experience for all trained skills. """
        return SkillTrained.objects.filter(slave=self).aggregate(Sum('exp'))['exp__sum']

    def get_skill(self, skill):
        """ Get current _skill_ level of Slave. """
        return SkillTrained.objects.get_skill_level(self, skill)

    def get_available_skills(self):
        """ Get a list of skills currently available for learning (using). """
        return SkillTrained.objects.get_available_skills(self)

    def get_trained_skills(self):
        """ Get a dictionary of available skills with level. """
        result = {}
        sk_all = SkillTrained.objects.get_available_skills(self)
        if len(sk_all) > 0:
            for s in sk_all:
                result[s] = SkillTrained.objects.get_skill_level(self, s)
        return result
        
    def add_skill_exp(self, skill, exp=1):
        """ Add some experience for current Skill. """
#        print("Adding {1} exp in {0} for slave {2}".format(skill, exp, self))
        if isinstance(skill, Skill):
            sk = skill
        elif isinstance(skill, int):
            sk = Skill.objects.get(pk=skill)
        elif isinstance(skill, str):
            sk = Skill.objects.get(name=skill)
        else:
            raise AttributeError("Skill must be <Skill> or int or str.")
        SkillTrained.objects.add_exp(self, sk, exp)

    """
    def ___set_skill(self, skill, exp):
        "" This is an admin function. Should hide it later. ""
        print(skill,exp)
        if not isinstance(skill, Skill):
            if isinstance(skill, int):
                sk = Skill.objects.get(pk=skill)
            else:
                raise AttributeError("Skill must be <Skill> or int")
        else:
            sk = skill
        SkillTrained.objects.set_st(self, sk, exp) """

########################
# TASK SECTON        

    def get_assignments(self, active=True):
        """ List assignments of Slave. If _active_ is False then show full list of assignment history. """
        return self.assignments.filter(date_released__isnull=True).all() if active\
            else self.assignments.all()

    def is_free(self):
        """ Returns True if Slave is not assigned to any task now. """
        return self.get_assignments(active=True).count() == 0

########################
# Slave update
    """
    def assign_to_task(self, task):
        print("Assigning {0} to task {1}".format(self, task))
        Assignment.objects.assign(slave=self, task=task)
    """

    def employ(self, task_type=None):
        """ Find job for the Slave. If task_type not given, then add some preferences. """

        if not self.is_free():
            raise TaskError("WARNING! {0} cannot be employed. Slave is busy already!".format(self))

        # If task type is not specified take all.
        if not task_type:
            task_type = TD.objects.all()

        # Find if there are open tasks of type in region
        available_tasks = Task.objects.filter(owner=self.owner,\
            _retrieved=False,
            type__in=task_type,location__region=self.get_region()).\
            order_by('-date_finish').all()

        # Filter tasks according to Slave skills and tasks free space
        tasks = [t for t in available_tasks if t.applicable_for_slave(self)\
            and t.has_open_vacancy() and t.has_free_space_in_location()]

        if len(tasks) > 0:
            task = tasks[0]
            a = Assignment.objects.assign(slave=self, task=task)
            return True if a else False
        return False
          

#################################
#################################
class RaceDefaults(models.Model):
    """ Settings table for default parameters when new slaves are born. """
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
