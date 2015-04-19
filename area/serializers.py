# AREA API Serializer #
from django.utils import timezone
from rest_framework import serializers
from area.models import Region, Location, LocationDirectory, LocationType

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'name', 'area', 'owner')

class LocationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationType
        fields = ('id', 'name')

class LocationDirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationDirectory
        fields = ('id', 'name', 'area', 'type')

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name', 'region', 'design')
        
### DETAILED SERIALIZERS ###
class RegionDetailSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Region
        fields = ('id', 'name', 'area', 'get_free_area', 'locations', 'owner')

class LocationDetailSerializer(serializers.ModelSerializer):
    free_area = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)

    def get_free_area(self, location):
        """ Calculated free area in Location. """
        return int(location.get_free_area())
        
    def get_type(self, location):
        """ Global location type. """
        return str(location.get_type())

    def get_owner(self, location):
        """ Owner of Region. """
        return int(location.get_owner().id)
        
    class Meta:
        model = Location
        fields = ('id', 'name', 'free_area', 'region', 'design', 'type', 'owner')
        