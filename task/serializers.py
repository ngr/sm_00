from django.forms import widgets
from django.utils import timezone
from rest_framework import serializers
from task.models import Task, TaskDirectory, Assignment
from slave.models import Slave

class AssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignment
        fields = ('id', 'task', 'slave', 'get_date_assigned', 'get_date_released')
        
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
      
    # Verify that Slave and Task are currently in the same Region.
        if not slave.get_location().get_region() == task.get_location().get_region():
            raise serializers.ValidationError("Region error. Slave is in wrong region.")
      
    # Verify that Slave is idle.
        if slave.get_assignments(active=True).count() > 0:
            raise serializers.ValidationError("Assignment error. Slave is busy.")
        
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
    _yield = serializers.FloatField(default=0.0)
    
    class Meta:
#        _date_start = serializers.DateTimeField('_date_start') or timezone.now()
        model = Task
        fields = ('id', 'type', 'is_retrieved', 'location', 'owner', '_fulfilled', '_yield', 'get_date_start', 'get_date_finish')
        
# FIXME NOW!
# This fucks the task on PUT request. :)))
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
