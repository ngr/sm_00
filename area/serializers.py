# AREA API Serializer #

from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import serializers
from rest_framework import pagination
from area.models import Region, Location, LocationDirectory, LocationType
from item.serializers import ItemShortSerializer

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'name', 'area', 'owner')

class LocationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationType
        fields = ('id', 'name')

class LocationDirectorySerializer(serializers.ModelSerializer):
    type_id = serializers.SerializerMethodField(read_only=True)

    def get_type_id(self, object):
        """ Rename parameter. """
        return object.id
    
    class Meta:
        model = LocationDirectory
        fields = ('id', 'name', 'area', 'type_id')

class LocationSerializer(serializers.ModelSerializer):
    design = serializers.SerializerMethodField(read_only=True)
    design_id = serializers.SerializerMethodField(read_only=True)
    type_id   = serializers.SerializerMethodField(read_only=True)
    region_id   = serializers.SerializerMethodField(read_only=True)
    
    def get_design(self, object):
        """ Generate directory for object. """
        return str(object.get_design())

    def get_design_id(self, object):
        """ Get design id. """
        return object.get_design().id

    def get_type_id(self, object):
        """ Global type of location Design. """
        return object.get_design().get_type().id

    def get_region_id(self, object):
        """ Get Region id. """
        return object.region.id

    class Meta:
        model = Location
        fields = ('id', 'name', 'design', 'design_id', 'type_id', 'region_id')
        
### DETAILED SERIALIZERS ###
class LocationDetailSerializer(LocationSerializer):
    free_area = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)
    
    def get_items(self, object):
        """ List of items. """
        items = object.get_items().all()
        serializer = ItemShortSerializer(items, many=True)
        return serializer.data

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
        fields = ('id', 'name', 'design', 'design_id', 'type', 'type_id', 'region_id', 'free_area', 'owner', 'items')

class RegionDetailSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    free_area = serializers.SerializerMethodField(read_only=True)
    def get_free_area(self, object):
        """ Calculated free area in Region. """
        return int(object.get_free_area())
    
    class Meta:
        model = Region
        fields = ('id', 'name', 'area', 'free_area', 'locations', 'owner')
