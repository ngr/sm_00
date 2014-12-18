import datetime
from random import random
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

        execution_time = 10 # Months. To be received from task type

        t = Task(slave=slave, date_start=timezone.now(), date_finish=(timezone.now() + datetime.timedelta(seconds=GAME_MONTH * execution_time)))
        t.save()
        return t

#    def retrieve(self):
#        print("Retrieving task:", self)


class FarmingManager(models.Manager):

    def assign(self, slave, plant):
        print("Assigning farming task to:", slave)
        t = Farming(slave=slave, date_start=timezone.now(), date_finish=(timezone.now() + datetime.timedelta(seconds=GAME_MONTH * plant.exec_time)), plant=plant)
        t.save()
        return t
        
    """    def retrieve(self):
        print("Retrieving task:", task)
        self.date_finish = timezone.now()
        self.save()

        return(self.get_yield())"""



class Task(models.Model):

    slave       = models.ForeignKey(Slave)
    date_start  = models.DateTimeField('Time of task start')
    date_finish = models.DateTimeField('Time of task finish')
    retrieved   = models.BooleanField(default=False)

    objects = TaskManager()

    def is_running(self):
        return self.date_finish > timezone.now()

    def __str__(self):
        return " " . join([str(self.slave), str(self.date_start), str(self.date_finish), str(self.retrieved)])


class RunningTask(models.Model):
    slave       = models.ForeignKey(Slave, related_name='+', db_index=True)
    task        = models.ForeignKey(Task)
    date_finish = models.DateTimeField('Time of task finish', db_index=True)

class Farming(Task):
    from task.farming import Plant

    plant       = models.ForeignKey(Plant)
    objects = FarmingManager()

    def get_yield(self):
        """ There can be several primary and secondary skills. The functions calculates the part of each one and the total output """

        print("Trying to yield from farming task")
        ps = self.plant.primary_skill
        ss = self.plant.secondary_skill.all()
        print("ps, ss =", ps, ss)
    
        pr_sl_skill = self.slave.get_skills(*[ps])
        sec_sl_skills = (self.slave.get_skills(*ss))
        print("Slave posesses:", pr_sl_skill, sec_sl_skills)

        print("Comparing:", ps, list(pr_sl_skill.keys()))
        if ps not in list(pr_sl_skill.keys()) or pr_sl_skill[ps] == 0:
            print("The slave doesn't posess primary skill. Looking for secondaries")
            print("Comparing:", ss, list(sec_sl_skills.keys()))
            if not any(s in list(sec_sl_skills.keys()) and sec_sl_skills[s] > 0 for s in ss):

                 print("The slave doesn't posess required skills. There is no yield!")
                 return 0
        
#        print("ps, ss ==== ", ps, ss)

#        sk_level = self.slave.skilltrained_set.all().get(Q(skill__in=ps) | Q(skill__in=ss))
#        print("Skill level:", sk_level)
        return 100

    def retrieve(self):
        print("Retrieving farming task:", self)
        self.retrieved = True
        self.save()
        return self.get_yield()



