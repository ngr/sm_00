### Task Serializers ###
from datetime import timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import serializers
from task.models import Task, TaskDirectory, Assignment
from item.models import Item
from slave.settings import *

class AssignmentSerializer(serializers.ModelSerializer):
    task_name = serializers.SerializerMethodField(read_only=True)
    task_workflow = serializers.SerializerMethodField(read_only=True)
    task_type = serializers.SerializerMethodField(read_only=True)
    date_assigned = serializers.SerializerMethodField(read_only=True)
    date_released = serializers.SerializerMethodField(read_only=True)
    # FIXME Add filter by owner and same for Slave selector.
    task    = serializers.PrimaryKeyRelatedField(queryset=Task.objects.filter(_retrieved=False))

    class Meta:
        model = Assignment
        fields = ('id', 'task', 'task_name', 'task_workflow', 'task_type', 'slave', 'date_assigned', 'date_released')
        
    def get_task_name(self, object):
        """ Get task name. """
        return str(object.task)

    def get_task_workflow(self, object):
        """ Get task workflow. """
        return object.task.type.id

    def get_task_type(self, object):
        """ Get task type. """
        return object.task.type.get_type_readable()

    def get_date_assigned(self, object):
        """ Get date. """
        return object.get_date_assigned()

    def get_date_released(self, object):
        """ Get date. """
        return object.get_date_released()

    def validate_slave(self, slave):
        """ Game logic and some authorization is checked here. """
        #print("Slave and Game Logic validation")
        
    # We make both validation for Slave and Game Logic in this
    # method, to avoid Task and Slave objects move here and there
    # many times.
    # We also assume that Task ownership was checked in POST
    # validation earlier and we consider Task owner to be the
    # current User.
        
        task = Task.objects.get(pk=self.initial_data['task'])
        
    # Verify that Slave and Task have the same owner.
        if slave.get_owner() != task.get_owner():
            #print("Owner of slave {0} is {1}, but owner of task {2} is {3}. Failed to assign!" \
            #    .format(slave, slave.get_owner(), task, task.get_owner()))
            raise serializers.ValidationError("Authorization error for this Slave.")

    # Verify that Task is running.
        if task.is_retrieved():
            raise serializers.ValidationError("Assignment error. Task is finished and retrieved.")

    # Verify that Task has open vacancy.
        if not task.has_open_vacancy():
            raise serializers.ValidationError("Assignment error. The maximum slaves are working on this task already.")

    # Verify that Task location has free space.
        if not task.has_free_space_in_location():
            raise serializers.ValidationError("Assignment error. The Task Location is overcrowded.")
            
    # Verify that Slave and Task are currently in the same Region.
        if not slave.get_location().get_region() == task.get_location().get_region():
            raise serializers.ValidationError("Region error. Slave is in wrong region.")
      
    # Verify that Slave is idle.
        if slave.get_assignments(active=True).count() > 0:
            raise serializers.ValidationError("Assignment error. Slave is busy.")
            
    # Verify that Slave is of appropriate age.
        if not slave.is_alive():
            raise serializers.ValidationError("Assignment error. Slave is dead.")
        if slave.is_baby():
            raise serializers.ValidationError("Assignment error. Slave is too young.")
            
    # Verify that Slave is qualified for this Task.
        slave_skills = slave.get_trained_skills()

        # Required primary and secondary skills.
        ps = task.get_primary_skill()

        if ps in list(slave_skills.keys()) and slave_skills[ps] > 0:
            print("The slave posesses primary skill.")
        else:
            raise serializers.ValidationError("Assignment error. Slave is not qualified for the task.")

        return slave

class TaskSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField(read_only=True)
    percent_completed = serializers.SerializerMethodField(read_only=True)
    active_assignments_count = serializers.SerializerMethodField(read_only=True)
    
    date_start  = serializers.DateTimeField(read_only=True)
    date_finish = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'type', 'percent_completed', 'active_assignments_count', 'is_retrieved', 'location', 'owner', 'date_start', 'date_finish')
        
    def get_name(self, object):
        """ Get readable name for Task. """
        return object.get_name_readable()

    def get_percent_completed(self, object):
        """ Calculate the percentage of finished. """
        # Farming tasks (time fixed)
        if object.get_type().is_time_fixed():
            # Return time delta (now-start)/(finish-start)
            return 100 if timezone.now() > object.get_date_finish() else \
                int((timezone.now() - object.get_date_start()) * 100 / \
                (object.get_date_finish() - object.get_date_start()))
               
        # Crafting, building tasks (work fixed)
        # Return work required - (fulfilled + current_work_per_day * timedelta(estimated_finish - last_update)
        elif object.get_type().is_work_fixed():
            work_units = object.get_type().get_param('work_units')
            fulfilled = object.get_fulfilled()
            # We get a result of actually fulfilled and saved amount of work
            result = 100.0 if fulfilled > work_units else \
                fulfilled * 100.0 / work_units
                
            # WARNING! The following can cause high loads. Monitor!
            # Check if somebody is working on this task now.
            running_assignments = object.get_assignments(running=True)
            if running_assignments.count() > 0:
            # Predict estimate of work done since last Task update.            
                last_update = object.get_date_updated()
                current_work_per_day = 0
                for a in running_assignments:
                    current_work_per_day += a.get_work_per_day()
                result += ((timezone.now() - last_update).seconds / GAME_DAY) * current_work_per_day
            #print("Task {0} is actually {1}% completed.".format(object, result))
            # We return floored int to avoid float number problems in API.
            return int(result)
        else:
            # In case some new task types appear.
            return 0
            
    def get_active_assignments_count(self, object):
        """ Shows the number of active assignments for the task. """
        return object.get_assignments(running=True).count()
    
    def  validate(self, data):
        """ A little gameplay logic validation. """
    # FIXME! Move this AWAY from serializer to Controller!!!
    # Verify sufficient materials.
        # print(data)
        # A little sleepy now to use cooler search in ordered dictionary
        # As long as data is OrderedDict we convert it to list and take
        # the required params only. We need location to determine the region
        # and the TaskWorkflow to get the recipe.
        for i in list(data.items()):
            if i[0] == 'type':
                type = i[1]
            elif i[0] == 'location':
                location = i[1]
                
        ingredients = type.get_param('ingredients')
        #print("INGREDIENTS, SELF:", ingredients, self)
 
        # As long as there might be no ingredient required, it might be False.
        # Otherwise we check if there are sufficient materials in storage.
        # This will be checked again later while saving.
        if ingredients:
            hq = location.region.get_locations('hq').first()
            for i in ingredients:
                if not Item.objects.exists(item=i.ingredient, location=hq, amount=i.amount):
                    raise serializers.ValidationError( "Not enough ingredient {0}".format(i.ingredient))
        return data
    
class TaskDetailSerializer(TaskSerializer):
    _yield       = serializers.FloatField(default=0.0, read_only=True)
    _fulfilled   = serializers.FloatField(default=0.0, read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)
    assignments  = AssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'type', 'percent_completed', 'active_assignments_count','is_retrieved', 'location', 'owner', '_fulfilled', '_yield', 'date_start', 'date_finish', 'date_updated', 'assignments')

# FIXME!
# This fucks the task on PUT request. :)))
# Never use PUT method to update anything in Task.
# Task interface should accept only "action".
    def validate__yield(self, value):
        """ Reset yield to zero if new Task posted. """
        # This is not critical if something is specified.
        # Simply reset it to zero according to Game logic.
        # Though this might not be RESTful. 
        if not self.instance:
            return 0.0

    def validate__fulfilled(self, value):
        """ Reset fulfilled to zero if new Task posted. """
        # This is not critical if something is specified.
        # Simply reset it to zero according to Game logic.
        # Though this might not be RESTful. 
        if not self.instance:
            return 0.0           
            
    def validate_location(self, location):
        """ Location must be of correct type and have minimum free space. """
        task_type = TaskDirectory.objects.get(pk=self.initial_data.get('type'))
#        print(task_type)

    # Authorize location.
    # This validation moved to VIEW class as we do not longer pass owner manually.
        #if not location.get_owner().id == int(self.initial_data.get('owner')):
            #print("Location owner: {0}, you are: {1}".format(location.get_owner(), self.initial_data.get('owner')))
            #raise serializers.ValidationError("You are not authorized for this location.")
    
    # Verify location type.
        if not location.get_type() == task_type.get_location_type():
            #print (location.get_type())
            raise serializers.ValidationError("Wrong type of location for the task.")
    
    # Verify free space in location.
        # The actual USE (reservation) of area will happen later on a 
        # per Slave (per Assignment) basis. Still we check for some minimum.
        #print("Location required: {0}, free: {1}".format(task_type.get_area_per_worker(), location.get_free_area()))
        if not location.get_free_area() >= task_type.get_area_per_worker():
            raise serializers.ValidationError("Not enough minimum free space in location.")

    # Succeeded with Location verification.
        return location

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

# WHAT IS THIS?????
#    def update(self, instance, validated_data):
#        instance._fulfilled     = validated_data.get('_fulfilled', instance._fulfilled)
#        instance._yield         = validated_data.get('_yield', instance._yield)
#        instance.save()
#        return instance

class TaskDirectorySerializer(serializers.ModelSerializer):
    """ Serialize TaskDirectory items for interface forms. """
    class Meta:
        model = TaskDirectory
        fields = ('id', 'name', 'location_type', 'area_per_worker', 'max_slaves')