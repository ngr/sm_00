### Skill Serializer ###
from rest_framework import serializers
from skill.models import Skill, SkillTrained
       
class SkillSerializer(serializers.ModelSerializer):
    """ Skill directory serializer. """
    
    class Meta:
        model = Skill
        fields = ('id', 'name', 'primary_attribute', 'difficulty', 'required_skills')

class SkillTrainedSerializer(serializers.ModelSerializer):
    """ Experience of Slaves in Skills. """
    skill   = serializers.CharField(read_only=True)
    level   = serializers.SerializerMethodField(read_only=True)
    exp     = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model  = SkillTrained
        fields = ('skill', 'level', 'exp')

    def get_level(self, object):
        """ Get calculated level of Skill according to exp. """
        return object.get_skill_level()

    def get_exp(self, object):
        """ Get gained experience for Skill. """
        return object.get_skill_exp()
