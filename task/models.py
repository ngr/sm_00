import datetime
from random import random, randrange
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.core.files.storage import FileSystemStorage

from slave.settings import *
from slave.models import Slave
from skill.models import Skill

class TaskManager(models.Manager):

    def assign(self, slave, task_type):

        print(Task.objects.filter(slave=slave, date_finish__gt=timezone.now()))

        execution_time = 15 # Months. To be received from task type

        t = Task(slave=slave, date_start=timezone.now(),\
                date_finish=(timezone.now() + datetime.timedelta(seconds=GAME_DAY * execution_time)))
        t.save()
        return t

#####################################
class FarmingManager(models.Manager):

    def assign(self, slave, plant):
        print("Assigning farming task to:", slave)
        t = Farming(slave=slave, date_start=timezone.now(), date_finish=(timezone.now() + datetime.timedelta(seconds=GAME_MONTH * plant.get_exec_time())), plant=plant)
        t.save()
        return t
        
#####################################
class Task(models.Model):

    slave       = models.ForeignKey(Slave)
    date_start  = models.DateTimeField('Time of task start')
    date_finish = models.DateTimeField('Time of task finish')
    retrieved   = models.BooleanField(default=False)
#   task_type   = models.PositiveSmallInteger(null=True)

    objects = TaskManager()

    def is_running(self):
        return self.date_finish > timezone.now()

    def __str__(self):
        return " " . join([str(self.slave), str(self.date_start), str(self.date_finish), str(self.retrieved)])

    def retrieve(self):
        print("Retrieving task:", self)
        self.retrieved = True
        self.save()
        return self.get_yield()

    def get_type(self):
        """ Returns readable type of task object """
        for t in TASK_TYPES:
            if hasattr(self, t[0]):
                return t[1]
        return False

    def get_details(self):
        """ Returns defaul str for template """
        return ""

#####################################
class RunningTask(models.Model):
    slave       = models.ForeignKey(Slave, related_name='+', db_index=True)
    task        = models.ForeignKey(Task)
    date_finish = models.DateTimeField('Time of task finish', db_index=True)

#####################################
class Farming(Task):
    from task.farming import Plant

    plant       = models.ForeignKey(Plant)
    objects = FarmingManager()

#    def __init__(self, *args, **kwargs):
#        super().task_type = 1

    def get_yield(self, strict=False):
        """ There can be several primary and secondary skills. 
        The functions calculates the part of each one and the total output.
        Primary skill = 50%, Secondary split by number. This results in base_yield.
        Bonuses may add extra. """

        print("Trying to yield from farming task")
        ps = self.plant.primary_skill
        ss = self.plant.secondary_skill.all()
        print("ps, ss =", ps, ss)
    
        slave_skills = self.slave.get_trained_skills()
#        sec_sl_skills = (self.slave.get_skills(*ss))
        print("Slave posesses:", slave_skills)

        print("Comparing:", ps, list(slave_skills.keys()))

        if ps not in list(slave_skills.keys()) or slave_skills[ps] == 0:
            print("The slave doesn't posess primary skill. Looking for secondaries")
            slave_skills[ps] = 0 # Should be set by Slave obj, but this is for safety
            if not any(s in list(slave_skills.keys()) and slave_skills[s] > 0 for s in ss):

                 print("The slave doesn't posess required skills. There is no yield!")
                 return 0

        result = 0
        by = self.plant.base_yield
        print("Base yield:", by)
        result += (by * (slave_skills[ps] / 100.0) * PRIMARY_SKILL_FARMING_VALUE)
        print("Primary skill harvested:", result)

        ss_part = SECONDARY_SKILLS_FARMING_VALUE / ss.count()

        for s in ss:
            result += (by * (slave_skills[s] / 100.0) * ss_part)
            print("Secondary skill {0} added some yield with result: {1}".format(s, result))

        if not strict:
            result += (result * (randrange(-YIELD_RANDOMIZER, YIELD_RANDOMIZER) / 100.0))
        


        return (self.plant.get_yield_type(), result)

    def get_specific_details(self):
        r = ""
        r += self.plant.name
        r += " estimated: " + str(self.get_yield())
        return r

