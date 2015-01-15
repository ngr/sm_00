import datetime
from random import random, randrange, choice
from django.db import models
from django.utils import timezone

from django.core.exceptions import ValidationError
from slave.logic import AssignmentError, TaskError

from slave.helpers import *
from slave.settings import *


class AssignmentManager(models.Manager):

    def get_slave_assignments(self, slave, active=True):
        """ Return a list of assignments for Slave """
        return Assignment.objects.filter(slave=slave, _date_released__isnull=True) if active\
                else Assignment.objects.filter(slave=slave)
    
    def check_slave_idle(self, slave, totally=True):
        """ Check if Slave has no job. Totally means not even self-assigned job. """
        return True if self.get_slave_assignments(slave).count() == 0 else False

    def check_slave_trained(self, slave, task):
        """ Check if Slave possesses required skills for this task """
        
        ps = task.get_primary_skill()
        ss = task.get_secondary_skill()

        slave_skills = slave.get_trained_skills()

        if ps in list(slave_skills.keys()) and slave_skills[ps] > 0:
            print("The slave posesses primary skill.")
            return True
        elif any(s in list(slave_skills.keys()) and slave_skills[s] > 0 for s in ss):
                print("The slave posesses some secondary skill.")
                return True
        else:
            return False

    def check_slave_location(self, slave, task):
        """ Check if Slave is in the same Region for Task """
        return slave.get_location().get_region() == task.get_location().get_region()

    def assign(self, task, slave):
        """ Perform the necessary checks and make Assignment """
        if not self.check_slave_location(slave, task):
            raise AssignmentError("Slave in wrong region")

        if not self.check_slave_idle(slave, totally=True):
            raise AssignmentError("Slave is busy")

        if not self.check_slave_trained(slave, task):
            raise AssignmentError("Slave is not trained for this")
        
    # If Task is not yet saved - do it now.
        if task._state.adding:
            task.save()

        a = Assignment(slave=slave, task=task)
        a.save()

        print("Successfully assigned")

class TaskManager(models.Manager):
    """ Operations on multiple Tasks """

    def auth_get_task(self, owner, task=None):
        """ Return Task or all tasks of 'owner' """
        args = ()
        kwargs = {}

        if task:
            kwargs['pk'] = task


# This should be the last param
        kwargs['_owner'] = owner
        return self.filter(*args, **kwargs)


    def get_finished(self, ttype=None):
        """ Return all finished not yet retrieved tasks """
        if not ttype:
            print("Return all non-retrieved tasks")
            return Task.objects.all().filter(_retrieved=0, _date_finish__lte=timezone.now()).all()
        else:
            print("Returning all tasks of type", ttype)
            return Task.objects.all().filter(_type=ttype, _retrieved=0, _date_finish__lte=timezone.now()).all()

    def get_running_available(self, ttype=None):
        """ Return running tasks with free working places """
        pass



class TaskDirectory(models.Model):
    _name   = models.CharField(max_length=127)
    _location_type = models.CharField(max_length=127, choices=LOCATION_TYPES, blank=True)

    _exec_time  = models.PositiveIntegerField(default=1)
    _min_slaves = models.PositiveIntegerField(default=1)
    _max_slaves = models.PositiveIntegerField(default=1)

    _primary_skill = models.ForeignKey('skill.Skill', related_name='+')
    _secondary_skill   = models.ManyToManyField('skill.Skill', related_name='+')

    def __str__(self):
        return self._name


    def get_type(self):
        """ Return list of types relative to TaskType """
        for t in TASK_DIRECTORIES:
            if hasattr(self, t[0]):
                    print("The type of task is", t[1], t[0])
                    return t[0]
        return False

    def get_param(self, param):
        """ Return the requested 'param' of 'itype' child """
        itype = self.get_type()
#        if not isinstance(itype, str) or not isinstance(param, str):
#            raise TypeError("Attributes should be strings")

#        itype = clean_string_title(itype)
        print(itype)
        t = [k[0] for k in TASK_DIRECTORIES if k[0] == itype]
        if len(t) == 0:
            raise AttributeError("Invalid attribute 'itype'")

        child_type = getattr(self, t[0])
        get_method = getattr(child_type, ('get_' + clean_string_lower(param)))
        return get_method()

    def get_location_type(self):
        return self._location_type

    def get_exec_time(self):
        return self._exec_time

    def get_min_slaves(self):
        return self._min_slaves

    def get_max_slaves(self):
        return self._max_slaves

    def get_primary_skill(self):
        if self._primary_skill:
            return self._primary_skill
        else:
            return False

    def get_secondary_skill(self):
        if self._secondary_skill.all().exists():
            return self._secondary_skill.all()
        else:
            return []


class FarmingTaskDirectory(TaskDirectory):
    from task.farming import Plant

    _plant = models.ForeignKey('Plant')


    def get_plant(self):
        return self._plant
#############
# We put yeild methods to this class as far as they are specific to task types
# This might be a bad idea, but it is specified.
# The method receives a parent TASK object
    def get_yield(self, task, strict=False):
        """ There can be several primary and secondary skills.
        The functions calculates the part of each one and the total output.
        Primary skill = 50%, Secondary split by number. This results in base_yield.
        Bonuses may add extra. """

        print("Trying to yield from farming task")
        print("Plant is:", self.get_plant())
        ps = self.get_primary_skill()
        ss = self.get_secondary_skill()
        print("ps, ss =", ps, ss)

        print("Now task specific stuff")
        for a in task.assignment_set.all():
            if a.is_running:
                a.release()

        slave_skills = a.slave.get_trained_skills()
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





class Task(models.Model):
    _type   = models.ForeignKey(TaskDirectory)
    _date_start  = models.DateTimeField()
    _date_finish = models.DateTimeField()

    _location   = models.ForeignKey('area.Location')

    _owner      = models.ForeignKey('auth.User')
    _retrieved  = models.BooleanField(default=False)

    _yield      = models.FloatField(default=0.0)

    objects     = TaskManager()

#    _primary_skill = models.ForeignKey('skill.Skill', related_name='+')
#    _secondary_skill   = models.ManyToManyField('skill.Skill', related_name='+')


    def get_test(self):
        pass

    def __str__(self):
        return " - ".join([str(self.id), str(self._type)])

    def get_type(self):
        return self._type

    def get_location(self):
        return self._location

    def get_region(self):
        return self.get_location().get_region()

    def get_owner(self):
        return self._owner

    def auth_allowed(self, user):
        """ Check permissions to access object """
        return True if self.get_owner() == user else False

    def is_retrieved(self):
        return self._retrieved

    def is_finished(self):
        return self.get_date_finish() <= timezone.now()


    def get_primary_skill(self):
        return self._type.get_primary_skill()

    def get_secondary_skill(self):
        return self._type.get_secondary_skill()

    def get_date_start(self):
        return self._date_start

    def get_date_finish(self):
        return self._date_finish

    def get_assignments(self, running=False):
        return self.assignment_set.all() if not running else\
                self.assignment_set.all().filter(_date_released__isnull=True)

    def has_open_vacancy(self):
        """ Returns if there are free working places """
        return self.get_assignments().count() < self.get_type().get_max_slaves()

    def get_farming_yield_item(self):
        return self.get_type().get_param('plant').get_yield_item()

    def get_yield(self):
        return self._yield
#######################
# SET VALUES
#######################
    def add_yield(self, y=1):
        if not y:
            return False

        y = fit_to_range_float(y, minv=0)
        if not y:
            raise AttributeError("Yield must be positive float")

        self._yield += y

#######################
# OTHER
#######################
    def save(self, *args, **kwargs):
        """ We save _dates automatically with no need to override """
        self.clean()
        if not self._date_start:
            self._date_start = timezone.now()
        self._date_finish = self.calculate_date_finish()
        super(Task, self).save(*args, **kwargs)

    def calculate_date_finish(self):
        """ Automatically calculates finish time of task.
            This is saved to optimize filter for robots """
        return self.get_date_start() + datetime.timedelta(seconds=(self.get_type().get_exec_time() * GAME_DAY))
         
    def clean(self):
        """ Check the location type vs required one for this type of task """
        if not self.get_location().get_type() == self.get_type().get_location_type():
#                [i[1] for i in LOCATION_TYPES if i[0] == self.get_type().get_location_type()][0]:
#            print(self.get_location().get_type())
#            print(self.get_type().get_location_type())
#            print([i[1] for i in LOCATION_TYPES if i[0] == self.get_type().get_location_type()])
            raise AssignmentError("Wrong type of location")

    def retrieve(self):
        print("Retrieving task:", self)

        if not self.is_finished():
            raise TaskError("You can retrieve only finished tasks")

        print("Cancelling assignments")
        current_assignments = self.get_assignments(running=True)
        if len(current_assignments) > 0:
            for a in current_assignments:
                print("{0} is released".format(a.get_slave()))
                a.release()
        else:
            print("No slaves to release")

        print("Retrieving yield")
#        child = getattr(self.get_type(),self.get_type().get_type())
        # we pass self to this typespecific method with some doubts, still we do.
        # The calculation is really task specific and we do not want an extra subclass tree.
#       task_yield = child.get_yield(self)
#        print(self.get_yield_farming())
        
        retr = self.get_yield_farming()
        print(retr)

        
        self.add_yield(retr[1])
        self._retrieved = True
#        self.save()

        ### Saving items retrieved
        amount = round(self.get_yield())
        item   = self.get_farming_yield_item()

        print("Retrieved a total {0} of {1}".format(amount, item))

        try:
            self.get_region().put_to_warehouse(item, amount)
        except ItemError:
            print("Some shit while putting item to warehouse")

        self.save() 
        return 

    def get_yield_farming(self, strict=False):
        """ There can be several primary and secondary skills.
        The functions calculates the part of each one and the total output.
        Primary skill = 50%, Secondary split by number. This results in base_yield.
        Bonuses may add extra. """

        print("Trying to yield from farming task")
#        print("Plant is:", self.get_type().farmingtaskdirectory.get_plant())
        ps = self.get_type().get_primary_skill()
        ss = self.get_type().get_secondary_skill()

        print("Now task specific stuff")
        cummulative_result = 0
        for a in self.get_assignments():
            a.release()

            slave_skills = a.get_slave().get_trained_skills()
#           sec_sl_skills = (self.slave.get_skills(*ss))
            print("Slave %s posesses:" % (str(a.get_slave())),  slave_skills)

            print("Comparing:", ps, list(slave_skills.keys()))

            if ps not in list(slave_skills.keys()) or slave_skills[ps] == 0:
                print("The slave doesn't posess primary skill. Looking for secondaries")
                slave_skills[ps] = 0 # Should be set by Slave obj, but this is for safety
                if not any(s in list(slave_skills.keys()) and slave_skills[s] > 0 for s in ss):

                     print("The slave doesn't posess required skills. There is no yield!")
                     return 0

            result = 0
            by = self.get_type().farmingtaskdirectory.get_plant().get_base_yield()
            print("Base yield: {0}".format(by))
            result += (by * (slave_skills[ps] / 100.0) * PRIMARY_SKILL_FARMING_VALUE)
#            print(slave_skills[ps])
#            print((slave_skills[ps] / 100.0) * PRIMARY_SKILL_FARMING_VALUE)
            print("Primary skill harvested: {0}".format(result))
    
            ss_part = SECONDARY_SKILLS_FARMING_VALUE / ss.count()

            for s in ss:
                if s in list(slave_skills.keys()) and slave_skills[s] > 0:
                    result += (by * (slave_skills[s] / 100.0) * ss_part)
#                    print(slave_skills[s])
#                    print((slave_skills[s] / 100.0) * ss_part)
                    print("Secondary skill {0} added some yield with result: {1}".format(s, result))

            if not strict:
                result += (result * (randrange(-YIELD_RANDOMIZER, YIELD_RANDOMIZER) / 100.0))
            print("Slave %s added %s to cummulative result" % (str(a.get_slave()), str(result)))
            cummulative_result += result

        return (self.get_type().farmingtaskdirectory.get_plant().get_yield_item(), cummulative_result)

    def get_yield_crafting(self):
        pass

#    def get_slaves_involved(self):
#        print(self.assignment_set.slave.all())
#        return self.assignment_set.slave.all()


class Assignment(models.Model):
    """ This class controls assignments of Slaves to Tasks. """
    task     = models.ForeignKey(Task)
    slave    = models.ForeignKey('slave.Slave')

    _date_assigned = models.DateTimeField()
    _date_released = models.DateTimeField(null=True)

    objects = AssignmentManager()


    def get_task(self):
        return self.task

    def get_slave(self):
        return self.slave

    def get_date_assigned(self):
        return self._date_assigned

    def get_date_released(self):
        return self._date_released

    def get_duraton(self):
        if not self.get_date_released():
            return timezone.now() - self.get_date_assigned()
        else:
            return self.get_date_released() - self.get_date_assigned()

    def is_running(self):
        return False if self._date_released else True

    def get_estimated_yield(self):
        return " - "


    def save(self, *args, **kwargs):
        self.clean()
        if not self._date_assigned:
            print("Setting Assignment date")
            self._date_assigned = timezone.now()
        super(Assignment, self).save(*args, **kwargs)

    def clean(self):
        """ Check if Assignment is going to be valid """
        if not self.task.has_open_vacancy():
            raise AssignmentError("Too many slaves for this task")

    def release(self):
        
        if not self.is_running():
            print("Assignment is already released")
            return False
        print("Releasing assignment {0}".format(self))
        self._date_released = timezone.now()

        ps = self.task.get_primary_skill()
        ss = self.task.get_secondary_skill()
        slave_skills = self.slave.get_available_skills()

        exp = int( (datetime.timedelta.total_seconds(self.get_duraton()) / GAME_DAY) * BASE_EXP_PER_DAY )
      
        if ps in slave_skills:
            print("{0} gained {1} experience for {2}".format(self.slave, exp, ps))
            self.slave.add_skill_exp(ps, exp)

        for s in ss:
            if s in slave_skills:
                print("{0} gained {1} experience for {2}".format(self.slave, exp, s))
                self.slave.add_skill_exp(s, exp)

        self.save()





# Create your models here.
