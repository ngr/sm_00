from datetime import timedelta
from django.forms import widgets
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import serializers
from task.models import Task, TaskDirectory, Assignment
from slave.models import Slave
from area.models import Location
from slave.settings import *

class AssignmentSerializer(serializers.ModelSerializer):
    url     = serializers.SerializerMethodField(read_only=True)
    # FIXME Add filter by owner and same for Slave selector.
    task    = serializers.PrimaryKeyRelatedField(queryset=Task.objects.filter(_retrieved=False))

    class Meta:
        model = Assignment
        fields = ('id', 'url', 'task', 'slave', 'get_date_assigned', 'get_date_released')
        
    def get_url(self, object):
        """ Generate URL for object. """
        return reverse('api:assignment-detail', args=[object.id])
    
    def validate_slave(self, slave):
        """ Game logic and some authorization is checked here. """
        print("Slave and Game Logic validation")
        
    # We make both validation for Slave and Game Logic in this
    # method, to avoid Task and Slave objects move here and there
    # many times.
    # We also assume that Task ownership was checked in POST
    # validation earlier and we consider Task owner to be the
    # current User.
        
        task = Task.objects.get(pk=self.initial_data['task'])
        
    # Verify that Slave and Task have the same owner.
        if slave.get_owner() != task.get_owner():
            print("Owner of slave {0} is {1}, but owner of task {2} is {3}. Failed to assign!" \
                .format(slave, slave.get_owner(), task, task.get_owner()))
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
        ss = task.get_secondary_skill()

        if ps in list(slave_skills.keys()) and slave_skills[ps] > 0:
            print("The slave posesses primary skill.")
        elif any(s in list(slave_skills.keys()) and slave_skills[s] > 0 for s in ss):
            print("The slave posesses some secondary skill.")
        else:
            raise serializers.ValidationError("Assignment error. Slave is not qualified for the task.")

        return slave
    
class TaskSerializer(serializers.ModelSerializer):
#    assignments = AssignmentSerializer(many=True, read_only=False)
    _yield      = serializers.FloatField(default=0.0, read_only=True)
    _fulfilled  = serializers.FloatField(default=0.0, read_only=True)
    url         = serializers.SerializerMethodField(read_only=True)
    name        = serializers.SerializerMethodField(read_only=True)
    percent_finished = serializers.SerializerMethodField(read_only=True)
    # FIXME Learn to pass request to Serializer and use current user
#    location    = serializers.PrimaryKeyRelatedField(queryset=Location.objects.filter(region__owner=2))
    _date_start  = serializers.DateTimeField(read_only=True)
    _date_finish = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'url', 'type', 'percent_finished', 'is_retrieved', 'location', 'owner', '_fulfilled', '_yield', '_date_start', '_date_finish', 'date_updated')

    def get_url(self, object):
        """ Generate URL for object. """
        return reverse('api:task-detail', args=[object.id])

    def get_name(self, object):
        """ Get readable name for Task. """
        return object.get_name_readable()

    def get_percent_finished(self, object):
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

# FIXME!
# This fucks the task on PUT request. :)))
# Never use PUT method to update anithing in Task.
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
        if not location.get_owner().id == int(self.initial_data.get('owner')):
            print("Location owner: {0}, you are: {1}".format(location.get_owner(),
                    self.initial_data.get('owner')))
            raise serializers.ValidationError("Error. You are not authorized for this location.")
    
    # Verify location type.
        if not location.get_type() == task_type.get_location_type():
            print (location.get_type())
            raise serializers.ValidationError("Error. Wrong type of location for the task.")
    
    # Verify free space in location.
        # The actual USE (reservation) of area will happen later on a 
        # per Slave (per Assignment) basis. Still we check for some minimum.
        print("Location required: {0}, free: {1}".format(task_type.get_area_per_worker(),
                location.get_free_area()))
        if not location.get_free_area() >= task_type.get_area_per_worker():
            raise serializers.ValidationError("Error. Not enough minimum free space in location.")

    # Succeeded with Location verification.
        return location

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance._fulfilled     = validated_data.get('_fulfilled', instance._fulfilled)
        instance._yield         = validated_data.get('_yield', instance._yield)
        instance.save()
        return instance
