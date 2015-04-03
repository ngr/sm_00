### TASK application models ###
import datetime
from random import random, randrange, choice
from math import ceil, floor

from django.db import models
from django.utils import timezone
from model_utils.managers import InheritanceManager

from django.core.exceptions import ValidationError
from slave.logic import AssignmentError, TaskError

from slave.helpers import *
from slave.settings import *

class AssignmentManager(models.Manager):

    def get_slave_assignments(self, slave, active=True):
        """ Return a list of assignments for Slave """
        return Assignment.objects.filter(slave=slave, date_released__isnull=True) if active\
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
        
      # Save task again to update estimated _date_finish.
        task.save()

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
        kwargs['owner'] = owner
        return self.filter(*args, **kwargs)


    def get_finished(self, ttype=None):
        """ Return all finished not yet retrieved tasks """
        if not ttype:
            print("Return all non-retrieved tasks")
            return Task.objects.all().filter(_retrieved=0, _date_finish__lte=timezone.now()).all()
        else:
            print("Returning all tasks of type", ttype)
            return Task.objects.all().filter(type=ttype, _retrieved=0, _date_finish__lte=timezone.now()).all()

    def auth_get_running_available(self, owner, region=None, ttype=None):
        """ Return running tasks with free working places """
        #FIXME Make interactive check if task type has fixed execution time
        # We now suppose that _date_finish is updated for tasks well. DOesn't matter the type.
        # This task becomes quite complicated because of complex type inheritance.
        args = ()
        kwargs = {}
        
      # Add running filter
        kwargs['_retrieved'] = 0
        kwargs['_date_finish__gt'] = timezone.now()
      
      # Add region filter
      # We should get the Region instance here.
        if region:
            try:
                kwargs['location__in'] = region.get_locations()
            except:
                print("Task->auth_get_running_available() - Could not get region locations")
            

# This should be the last param
        kwargs['owner'] = owner
        return self.filter(*args, **kwargs)
        
class TaskDirectory(models.Model):
    _name   = models.CharField(max_length=127)
    _location_type = models.CharField(max_length=127, choices=LOCATION_TYPES, blank=True)
    _area_per_worker = models.PositiveIntegerField(default=1)

    _min_slaves = models.PositiveIntegerField(default=1)
    _max_slaves = models.PositiveIntegerField(default=1)

    _primary_skill = models.ForeignKey('skill.Skill', related_name='+')
    _secondary_skill   = models.ManyToManyField('skill.Skill', related_name='+')
    
    #objects = InheritanceManager()

    # FIXME Need some Meta here for exec_time or exec_work to be null. Not together.

    def __str__(self):
        return "{0}: {1}".format(self.get_type_readable(), self._name)


    def get_type(self):
        """ Return list of types relative to TaskType """
        for t in TASK_DIRECTORIES:
            if hasattr(self, t[0]):
                    #print("The type of task is", t[1], t[0])
                    return t[0]
        return False
        
    def get_type_readable(self):
        """ Return list of types relative to TaskType """
        for t in TASK_DIRECTORIES:
            if hasattr(self, t[0]):
                    #print("The type of task is", t[1], t[0])
                    return t[1]
        return False

    def is_time_fixed(self):
        """ The task is executed some fixed time. """
        # If a subtype has the _exec_time attribute then it has time limit
        try:
            return getattr(self, self.get_type())._exec_time is not None
        except AttributeError:
            return False

    def is_work_fixed(self):
        """ The task needs some fixed work to be done """
        # If a subtype has the _work_units attribute then it has work limit
        try:
            return getattr(self, self.get_type())._work_units is not None
        except AttributeError:
            return False

    def get_param(self, param):
        """ Return the requested 'param' of 'itype' child """
        try:
            return getattr(getattr(self, self.get_type()), ('get_' + clean_string_lower(param)))()
        except AttributeError:
            return False

        # The old way looks too complex and didn't catch exceptions
        #itype = self.get_type()
        #print(itype)
        #t = [k[0] for k in TASK_DIRECTORIES if k[0] == itype]
        #if len(t) == 0:
            #raise AttributeError("Invalid attribute 'itype'")

        #this is the old way:
        #child_type = getattr(self, t[0])
        #get_method = getattr(child_type, ('get_' + clean_string_lower(param)))
        #return get_method()

    """ Basic get() methods for TaskDirectory instance properties """
    def get_location_type(self):
        return self._location_type

    def get_area_per_worker(self):
        return self._area_per_worker

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
    """ General subtype of farming task types. """

    _yield_item  = models.ForeignKey('item.ItemDirectory')
    _base_yield  = models.PositiveSmallIntegerField(default=1)
    _exec_time   = models.PositiveSmallIntegerField(default=1)

    """ Basic get() methods for FarmingTaskDirectory properties. """
    def get_yield_item(self):
        return self._yield_item

    def get_base_yield(self):
        return self._base_yield

    def get_exec_time(self):
        return self._exec_time
    
#############
# We put yield methods to this class as far as they are specific to task types
# This might be a bad idea, but it is specified.
# The method receives a parent TASK object
"""    def get_yield(self, task, strict=False):
        " "" There can be several primary and secondary skills.
        The functions calculates the part of each one and the total output.
        Primary skill = 50%, Secondary split by number. This results in base_yield.
        Bonuses may add extra. "" "

        print("Trying to yield from farming task")
        ps = self.get_primary_skill()
        ss = self.get_secondary_skill()
        print("ps, ss =", ps, ss)

        print("Now task specific stuff")
        for a in task.assignment_set.all():
            if a.is_running:
                a.release()

        slave_skills = a.slave.get_trained_skills()
#        sec_sl_skills = (self.slave.get_skills(*ss))
        print("Slave possesses:", slave_skills)

        print("Comparing:", ps, list(slave_skills.keys()))

        if ps not in list(slave_skills.keys()) or slave_skills[ps] == 0:
            print("The slave doesn't posess primary skill. Looking for secondaries")
            slave_skills[ps] = 0 # Should be set by Slave obj, but this is for safety
            if not any(s in list(slave_skills.keys()) and slave_skills[s] > 0 for s in ss):

                 print("The slave doesn't posess required skills. There is no yield!")
                 return 0

        result = 0
        by = self.get_base_yield()
        print("Base yield:", by)
        result += (by * (slave_skills[ps] / 100.0) * PRIMARY_SKILL_FARMING_VALUE)
        print("Primary skill harvested:", result)

        ss_part = SECONDARY_SKILLS_FARMING_VALUE / ss.count()

        for s in ss:
            result += (by * (slave_skills[s] / 100.0) * ss_part)
            print("Secondary skill {0} added some yield with result: {1}".format(s, result))

        if not strict:
            result += (result * (randrange(-YIELD_RANDOMIZER, YIELD_RANDOMIZER) / 100.0))


        return (self.get_yield_type(), result) """

class CraftingTaskDirectory(TaskDirectory):
    """ General subtype of crafting task types. """

    item  = models.ForeignKey('item.ItemDirectory', related_name='yeild_item')
    _work_units  = models.PositiveIntegerField(default=1)
    
    ingredient    = models.ManyToManyField('item.ItemDirectory', through='item.ItemRecipe', through_fields=('task_type', 'ingredient'))

    def __str__(self):
        return str(self._name)

    """ Basic get() methods for CraftingTaskDirectory properties. """
    def get_item(self):
        return self.item    

    def get_yield_item(self):
        return self.item    

    def get_work_units(self):
        return self._work_units    

class BuildingTaskDirectory(TaskDirectory):
    """ General subtype of building task types. """

    _work_units  = models.PositiveIntegerField(default=1)
    
    building  = models.ForeignKey('area.BuildingType')
    material  = models.ManyToManyField('item.MaterialDirectory', through='area.BuildingMaterialRecipe', through_fields=('task_type', 'material'))

    """ Basic get() methods for CraftingTaskDirectory properties. """
    def __str__(self):
        return str(self.building) 

    def get_work_units(self):
        return self._work_units    
    
    def get_building(self):
        return self.building

    def get_yield_building(self):
        return self.building
    
    def get_material(self):
        return self.material

 
class Task(models.Model):
    _date_start  = models.DateTimeField()
    _date_finish = models.DateTimeField()

    _retrieved  = models.BooleanField(default=False)
    _yield      = models.FloatField(default=0.0)
    _fulfilled  = models.FloatField(default=0.0)

    type        = models.ForeignKey(TaskDirectory)
    location    = models.ForeignKey('area.Location')
    owner       = models.ForeignKey('auth.User', related_name='tasks')

    objects     = TaskManager()

    def get_test(self):
        pass

    def __str__(self):
        return " - ".join([str(self.id), str(self.type.get_type_readable())])

    def get_name_readable(self):
        """ Return string name to show Task name in API. """
        return " - ".join([str(self.id), str(self.type.get_type_readable())])
        
    def get_type(self):
        return self.type

    def get_type_readable(self):
        """ Get type directory (group of types). """
        return self.type.get_type_readable()

        

    def get_location(self):
        return self.location

    def get_region(self):
        return self.get_location().get_region()

    def get_owner(self):
        return self.owner

    def auth_allowed(self, user):
        """ Check permissions to access object """
        return True if self.get_owner() == user else False

    def is_retrieved(self):
        return self._retrieved

    def is_finished(self):
        return self.get_date_finish() <= timezone.now()


    def get_primary_skill(self):
        return self.type.get_primary_skill()

    def get_secondary_skill(self):
        return self.type.get_secondary_skill()

    def get_date_start(self):
        return self._date_start

    def get_date_finish(self):
        return self._date_finish

    def get_assignments(self, running=False):
        return self.assignments.all() if not running else\
                self.assignments.all().filter(date_released__isnull=True)

    def has_open_vacancy(self):
        """ Returns if there are free working places. """
        return self.get_assignments(running=True).count() < self.get_type().get_max_slaves()
    
    def has_free_space_in_location(self):
        """ Check if there is free space for more assignments. """
        required_area = self.type.get_area_per_worker()
        available_area = self.get_location().get_free_area()
        print("Location needs {0} area and currently has {1}.".format(required_area, available_area))
        return available_area > required_area

    def get_farming_yield_item(self):
        return self.get_type().get_param('plant').get_yield_item()

    def get_yield(self):
        return self._yield
        
    def get_fulfilled(self):
        return self._fulfilled
    
#######################
# UPDATE PROPERTIES
#######################
    def add_fulfilled(self, amount=0):
        """ Add some work_units when assignment is closed. """
        self._fulfilled += amount
        
        # Check if finished the task. Then force soon retrieve.
        if self._fulfilled >= self.type.get_param('work_units'):
            self._date_finish = timezone.now()
        
        self.save()
        
    def add_yield(self, y=0):
        """ Add some yield results when assignment is closed. """
        if not y:
            return False

        y = fit_to_range_float(y, minv=0)
        if not y:
            raise AttributeError("Yield must be positive float")

        self._yield += y
        self.save()

#######################
# OTHER
#######################
    def save(self, *args, **kwargs):
        """ We save _dates automatically with no need to override """
        self.clean()
        if not self._date_start:
            self._date_start = timezone.now()
        print("Setting _date_finish to: {0}".format(self.calculate_date_finish()))
        self._date_finish = self.calculate_date_finish()
        super(Task, self).save(*args, **kwargs)

    def calculate_date_finish(self):
        """ Automatically calculates estimated finish time of task.
            This is saved to optimize filter for robots """
        ### FIXME Need to complete this function!   
        
      # When the task is finished it also needs to save, so we return now()
        if self._retrieved:
            return timezone.now()
         
      # If task type has fixed exec time
        if self.type.is_time_fixed():
          # Return time.start + delta of execution
            return self.get_date_start() + \
                datetime.timedelta(seconds=(self.type.get_param('exec_time') * GAME_DAY))
        
      # Else if type has fixed worker
        elif self.type.is_work_fixed():
#            return timezone.now() + \
#                datetime.timedelta(seconds=(self.type.get_param('work_units') * GAME_DAY))
        
          # Get remaining amount of work
            work_left = self.type.get_param('work_units') - self.get_fulfilled()

          # Summarize estimated work from all assignments
            current_work_per_day = 0
            running_assignments = self.get_assignments(running=True)
#            print("RUNNING ASSIGNMENTS. Number: {0}. Start first: {1}. Start last: {2}.".format( \
#                running_assignments.count(), \
#                running_assignments.first().get_date_assigned(), \
#                running_assignments.last().get_date_assigned() \
#                ))
            for a in running_assignments:
              # Calculate estimated work per second
                current_work_per_day += a.get_work_per_day()

            print("CURRENT_WORK_PER_DAY", current_work_per_day)
          # Calculate remaining GAME_DAYs
            if current_work_per_day > 0:
                days_left = ceil(work_left / current_work_per_day)
            else:
                days_left = ceil(work_left)
            
          # Return Estimated time of finish.
          # We take the start time of the first assignment and calculate
          # with estimate work_per_day. In case we add new workers in the
          # middle of the process, we shall receive estimated time 
          # earlier than actual finish (even possibly time in the past).
          # This will run automated retriever one extra time and it will
          # add fulfilled work, refresh assignments and recalculate 
          # estimates in the proper way.
            if running_assignments.count() > 0:
                last_saved_time = running_assignments.first().get_date_assigned()
            else:
                last_saved_time = timezone.now()
                
            return last_saved_time + datetime.timedelta(seconds=(days_left * GAME_DAY))

         
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
            raise TaskError("Task is not finished yet.")

        if self.is_retrieved():
            raise TaskError("Task was already retrieved.")

        print("Cancelling assignments")
        current_assignments = self.get_assignments(running=True)
      # In case we did not yet finish, we shall assign the same slaves again.
        previous_slaves = []
        if len(current_assignments) > 0:
            for a in current_assignments:
                print("{0} is released".format(a.get_slave()))
                previous_slaves.append(a.get_slave())
                a.release()
        else:
            print("No Assignments to release")

        print("Previous Slaves: {0}".format(previous_slaves))

        print("Retrieving yield")
        print(self.type.get_type())
        
        if str(self.type.get_type()) == 'farmingtaskdirectory':
            self._retrieved = True
            self.finish_farming()
            
        elif str(self.type.get_type()) == 'craftingtaskdirectory':
          # Check if not all of the required work is finished.          
            print("Fullfilled {0} of {1}".format(self.get_fulfilled(),
                self.type.craftingtaskdirectory.get_work_units()))
            if self.get_fulfilled() < self.type.craftingtaskdirectory.get_work_units():
                print("Previous Slaves: {0}".format(previous_slaves))
                for s in previous_slaves:
                    print("Reassigning Slave {0} to Task {1}".format(s, self))
                    s.assign_to_task(self)
          # Otherwise finish the task
            else:
                self._retrieved = True
                self.finish_crafting()
                
        elif str(self.type.get_type()) == 'buildingtaskdirectory':
          # Check if not all of the required work is finished.  
            if self.get_fulfilled() < self.type.buildingtaskdirectory.get_work_units():
                for s in previous_slaves:
                    s.assign_to_task(self)

          # Otherwise finish the task
            else:
                self._retrieved = True
                self.finish_building()

        self.save() 
        return True

    def finish_farming(self):
        """ Put to warehouse farmed goods. """
        print("FINISH FARMING")
        amount_produced = 0
        item_produced = self.get_type().get_param('yield_item')
      
      # To get base amount produced the amount of fulfilled work  must be equal 
      # to base duration multiplied by PRIMARY_SKILL_WORK_VALUE * 100%
        base_work = self.get_type().get_param('exec_time')
        work_fulfilled = self.get_fulfilled() / base_work
        amount_produced = int(work_fulfilled * self.get_type().get_param('base_yield'))
        
        print("The task produced {0} work resulting in {1} of {2}".format(work_fulfilled, amount_produced, item_produced))
        
        try:
            self.get_region().put_to_warehouse(item_produced, amount_produced)
        except:
            print("Some shit while putting item to warehouse")
        
    def finish_crafting(self):
        """ Put to warehouse crafted items. """
        print("FINISH CRAFTING")
        item_produced = self.get_type().get_param('yield_item')
        amount_produced = floor(self.get_fulfilled() // self.get_type().get_param('work_units'))
        print("The task produced {0} work resulting in {1} of {2}".format(self.get_fulfilled(), amount_produced, item_produced))
    
      # Now put to warehouse
        try:
            self.get_region().put_to_warehouse(item_produced, amount_produced)
        except:
            print("Some shit while putting item to warehouse")


     
    def finish_building(self):
        """ Place new Location. """
        # This is the first draft version. We do not reserve area for location in advance. 
        # We simply create new Location in Region now.
        print("FINISH BUILDING")
        building_type = self.get_type().get_param('yield_building')
        new_location = self.get_region().create_location(type=building_type)

        
    def get_yield_farming(self, strict=False):
    # FIXME TO BE REMOVED FROM HERE!
        """ There can be several primary and secondary skills.
        The functions calculates the part of each one and the total output.
        Primary skill = 50%, Secondary split by number. This results in base_yield.
        Bonuses may add extra. """

        print("Trying to yield from farming task")
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
            result += (by * (slave_skills[ps] / 100.0) * PRIMARY_SKILL_WORK_VALUE)
#            print(slave_skills[ps])
#            print((slave_skills[ps] / 100.0) * PRIMARY_SKILL_FARMING_VALUE)
            print("Primary skill harvested: {0}".format(result))
    
            ss_part = SECONDARY_SKILLS_WORK_VALUE / ss.count()

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
        

class Assignment(models.Model):
    """ This class controls assignments of Slaves to Tasks. """
    task     = models.ForeignKey(Task, related_name='assignments')
    slave    = models.ForeignKey('slave.Slave', related_name='assignments')

    date_assigned = models.DateTimeField()
    date_released = models.DateTimeField(null=True)

    objects = AssignmentManager()

    class Meta:
        unique_together = (("slave", "date_released"),)

    def get_task(self):
        return self.task

    def get_slave(self):
        return self.slave

    def get_date_assigned(self):
        return self.date_assigned

    def get_date_released(self):
        return self.date_released

    def get_duration(self):
        if not self.get_date_released():
            return timezone.now() - self.get_date_assigned()
        else:
            return self.get_date_released() - self.get_date_assigned()

    def is_running(self):
        return False if self.date_released else True

    def get_estimated_yield(self):
        return " - "
 

    def save(self, *args, **kwargs):
        self.clean()
        if not self.date_assigned:
            print("Setting Assignment date")
            self.date_assigned = timezone.now()
        super(Assignment, self).save(*args, **kwargs)

    def clean(self):
        """ Check if Assignment is going to be valid """
        # We check if_running to skip this verification
        # while saving on assignment.release()
        if not self.task.has_open_vacancy() and self.is_running():
            raise AssignmentError("Too many slaves for this task")

        if not self.task.has_free_space_in_location():
            raise AssignmentError("There is no free space in Location of this task")

    def release(self):
        """ Releasing the Slave from Assignment (and closing the Assignment).
        Yield and production are calculated here. Slave new Experience also. """
    # Check if Assignment is not released already 
        if not self.is_running():
            print("Assignment is already released")
            return False
        print("Releasing assignment {0}".format(self))
        # Now the duration will count till this date_released point.
        # In case of bugs your may need to extra save() here.
        self.date_released = timezone.now()
        
    ### Updating slave Skill Experience
        # We use all skills available for the Slave at the moment.
        # And for any of them he will get some experience
        slave_skills = self.get_slave().get_available_skills()
        ps = self.task.get_primary_skill()
        ss = self.task.get_secondary_skill()
        
        # We use only full Game days. If the assignment was shorter 
        # - no training and no fulfilled work happens. 
        # This should prevent any possible short assignments bugs.
        duration = datetime.timedelta.total_seconds(self.get_duration()) / GAME_DAY
        print("The total duration of assignment was {0} GAME DAYS".format(duration))
        
      # WORK REQUIRED
      # Eexperience should also depend on other more skilled slaves working simultaneously.
        # Experience directly depends on assignment duration
        exp  = int(duration * BASE_EXP_PER_DAY)
        # The part of each secondary skill output depends on their number.
        exp_for_secondary_skill = int((duration * SECONDARY_SKILLS_EXP_PER_DAY) / ss.count())

        # Adding exp for Primary Skill.
        if ps in slave_skills:
            print("{0} gained {1} experience for {2}".format(self.get_slave(), exp, ps))
            self.slave.add_skill_exp(ps, exp)
            
        for s in ss:
            if s in slave_skills:
                print("{0} gained {1} experience for {2}".format(self.slave, exp_for_secondary_skill, s))
                self.slave.add_skill_exp(s, exp_for_secondary_skill)
                
        
        # Calculate and update work_units for parent Task.
#        print(duration, self.get_work_per_day())
        assignment_work = duration * self.get_work_per_day()
        print("Total work produced by Assignment is: {0}".format(assignment_work))

        self.task.add_fulfilled(amount=assignment_work)
        self.save()
        return True
        
    def get_work_per_day(self):
        """ Return the amount of work per minimum assignment time unit (GAME_DAY). """
        
        ps = self.task.get_primary_skill()
        ss = self.task.get_secondary_skill()
        slave_skills = self.get_slave().get_available_skills()

        assignment_work = 0.0
      # Calculate result work for Primary skill
        if ps in slave_skills:
            
            skill_level = self.get_slave().get_skill(ps)
            assignment_work += skill_level * 0.01 * PRIMARY_SKILL_WORK_VALUE
            # print("Skill {0} produced {1} of work units".format(ps, skill_work))

      # The part of each secondary skill output depends on their number
        part_of_secondary_skill = SECONDARY_SKILLS_WORK_VALUE / ss.count()
      
      # Calculate result work for Secondary skills
        for s in ss:
            if s in slave_skills:
                skill_level = self.get_slave().get_skill(s)
                assignment_work += skill_level * 0.01 * part_of_secondary_skill
                # print("Skill {0} produced {1} of work units".format(s, skill_work))
        
        return assignment_work
