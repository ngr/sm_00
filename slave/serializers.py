### Slave Serializers ### 

from datetime import timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import serializers
from slave.models import Slave
from skill.models import Skill, SkillTrained
from area.models import Location
from task.serializers import AssignmentSerializer
from skill.serializers import SkillTrainedSerializer

from slave.settings import *

class SlaveSerializer(serializers.ModelSerializer):
    """ Basic serializer for listing Slaves. """
    name        = serializers.SerializerMethodField(read_only=True)
    age         = serializers.SerializerMethodField(read_only=True)
    sex         = serializers.CharField(read_only=True)
    race        = serializers.IntegerField(read_only=True)
    exp         = serializers.SerializerMethodField(read_only=True)
    free        = serializers.SerializerMethodField(read_only=True)
    region_id   = serializers.SerializerMethodField(read_only=True)
    assignment  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Slave
        fields = ('id', 'name', 'age', 'sex', 'race', 'exp', 'region_id', 'free', 'assignment')
        
    def get_name(self, object):
        """ Get name of Slave. """
        return object.get_name()
        
    def get_age(self, object):
        """ Get Age of Slave. """
        return object.get_age()

    def get_exp(self, object):
        """ Get Total experience of Slave. """
        return object.get_total_exp()

    def get_free(self, object):
        """ Check id Slave has running assignments. """
        return object.is_free()
    
    def get_region_id(self, object):
        """ Return ID of current Slave Region. """
        return object.location.region.id

    def get_assignment(self, object):
        """ Get running assignment. """
        assignment = object.assignments.last()
        return AssignmentSerializer(assignment, read_only=True).data if assignment.is_running() else None

class SlaveDetailSerializer(SlaveSerializer):
    """ A lot of attributes associated with the Slave. """
    
    assignments  = serializers.SerializerMethodField(read_only=True)
    skills       = serializers.SerializerMethodField(read_only=True)
    intelligence = serializers.IntegerField(read_only=True)
    strength     = serializers.IntegerField(read_only=True)
    agility      = serializers.IntegerField(read_only=True)
    charisma     = serializers.IntegerField(read_only=True)
    
    class Meta:
        model  = Slave
        fields = ('id', 'name', 'age', 'sex', 'race', 'exp', 'region_id', 'free', 'date_birth',\
            'intelligence', 'strength', 'agility', 'charisma', 'happiness', 'assignments', 'skills')
            
    def get_assignments(self, object):
        """ Get assignments of Slave. """
        serializer = AssignmentSerializer(object.assignments.all().filter(date_released=None), many=True, read_only=True)
        return serializer.data
    
    def get_skills(self, object):
        """ Get serialized list of current Slave Skills. """
        serializer = SkillTrainedSerializer(object.get_skills().all(),  many=True, read_only=True)
        return serializer.data
