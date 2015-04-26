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
    url         = serializers.SerializerMethodField(read_only=True)
    age         = serializers.SerializerMethodField(read_only=True)
    free        = serializers.SerializerMethodField(read_only=True)
    location    = serializers.PrimaryKeyRelatedField(queryset=Location.objects.filter(design__type=1))

    class Meta:
        model = Slave
        fields = ('id', 'url', 'get_name', 'location', 'age', 'free')
        
    def get_url(self, object):
        """ Generate URL for object. """
        return reverse('api:slave-detail', args=[object.id])
        
    def get_age(self, object):
        """ Get Age of Slave. """
        return object.get_age()

    def get_free(self, object):
        """ Check id Slave has running assignments. """
        return object.is_free()

class SlaveDetailSerializer(SlaveSerializer):
    """ A lot of attributes associated with the Slave. """
    
    assignments = serializers.SerializerMethodField(read_only=True)
    skills      = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model  = Slave
        fields = ('id', 'url', 'get_name', 'location', 'age', '_date_birth', 'assignments', 'skills')
            
    def get_assignments(self, object):
        """ Get assignments of Slave. """
        serializer = AssignmentSerializer(object.assignments.all().filter(date_released=None), many=True, read_only=True)
        return serializer.data
    
    def get_skills(self, object):
        """ Get serialized list of current Slave Skills. """
        serializer = SkillTrainedSerializer(object.get_skills().all(),  many=True, read_only=True)
        return serializer.data
