from django.db import models


from slave.helpers import *
from slave.settings import *


class TaskDirectory(models.Model):
    _name   = models.CharField(max_length=127)

    _exec_time  = models.PositiveIntegerField(default=1)
    _min_slaves = models.PositiveIntegerField(default=1)
    _max_slaves = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self._name

    def get_type(self):
        """ Return list of types relative to TaskType """
        for t in TASK_DIRECTORIES:
            if hasattr(self, t[0]):
                    print("The type of task is", t[1], t[0])
                    return t[1]
        return False

    def get_param(self, itype, param):
        """ Return the requested 'param' of 'itype' child """
        if not isinstance(itype, str) or not isinstance(param, str):
            raise TypeError("Attributes should be strings")

        itype = clean_string_title(itype)
        t = [k[0] for k in TASK_DIRECTORIES if k[1] == itype]
        if len(t) == 0:
            raise AttributeError("Invalid attribute 'itype'")

        child_type = getattr(self, t[0])
        get_method = getattr(child_type, ('get_' + clean_string_lower(param)))
        return get_method()



class FarmingTaskDirectory(TaskDirectory):
    from task.farming import Plant

    _plant = models.ForeignKey('Plant')


    def get_plant(self):
        return self._plant
    





class Task(models.Model):
    _type   = models.ForeignKey(TaskDirectory)
    _date_init  = models.DateTimeField()
    
    _retrieved  = models.BooleanField(default=False)


    def __str__(self):
        return " - ".join([self._type, self._date_init])


class Assignment(models.Model):
    task     = models.ManyToManyField(Task)
    slave    = models.ManyToManyField('slave.Slave')




# Create your models here.
