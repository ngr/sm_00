# AREA API Serializer #
from django.utils import timezone
from rest_framework import serializers
from area.models import Area, Location

class FarmingFieldSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = FarmingField
        fields = ('id')
