# AREA API Serializer #

from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import serializers
from rest_framework import pagination
from area.models import Region, Location, LocationDirectory, LocationType
from item.serializers import ItemShortSerializer

class RegionSerializer(serializers.ModelSerializer):
    url    = serializers.SerializerMethodField(read_only=True)

    def get_url(self, object):
        """ Generate URL for object. """
        return reverse('api:region-detail', args=[object.id])

    class Meta:
        model = Region
        fields = ('id', 'name', 'url', 'area', 'owner')

class LocationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationType
        fields = ('id', 'name')

class LocationDirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationDirectory
        fields = ('id', 'name', 'area', 'type')

class LocationSerializer(serializers.ModelSerializer):
    url    = serializers.SerializerMethodField(read_only=True)

    def get_url(self, object):
        """ Generate URL for object. """
        return reverse('api:location-detail', args=[object.id])

    class Meta:
        model = Location
        fields = ('id', 'name', 'url', 'region', 'design')
        
### DETAILED SERIALIZERS ###
class RegionDetailSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    free_area = serializers.SerializerMethodField(read_only=True)
    def get_free_area(self, object):
        """ Calculated free area in Region. """
        return int(object.get_free_area())
    
    class Meta:
        model = Region
        fields = ('id', 'name', 'area', 'free_area', 'locations', 'owner')

class LocationDetailSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'name', 'free_area', 'region', 'design', 'type', 'owner', 'items')
        