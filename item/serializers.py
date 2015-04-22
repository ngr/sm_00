from django.forms import widgets
from django.core.urlresolvers import reverse
from rest_framework import serializers
from item.models import Item, ItemBaseParam

class ItemParamSerializer(serializers.ModelSerializer):
    """ Used to serialize ItemParamDirectory objects. """
    name    = serializers.CharField()
    value   = serializers.CharField()
    
    class Meta:
        model  = ItemBaseParam
        fields = ('name', 'value')

class ItemShortSerializer(serializers.ModelSerializer):
    """ Used to serialize Items for API. """
    name   = serializers.SerializerMethodField(read_only=True)
    url    = serializers.SerializerMethodField(read_only=True)
    
    def get_url(self, object):
        """ Generate URL for object. """
        return reverse('api:item-detail', args=[object.id])
     
    def get_name(self, object):
        """ Return some readable name for Item. """
        return "{0}".format(object.get_type().__str__())
        
    class Meta:
        model = Item
        fields = ('id', 'name', 'url', 'itype', 'amount', 'location')

class ItemSerializer(serializers.ModelSerializer):
    """ Used to serialize Items for API. """
    params = serializers.SerializerMethodField(read_only=True)
    name   = serializers.SerializerMethodField(read_only=True)

    def get_params(self, object):
        """ Get ItemDirectory params. """
        base_params_qs = object.itype.get_param().all()
        serializer = ItemParamSerializer(base_params_qs, many=True)
        return serializer.data
     
    def get_name(self, object):
        """ Return some readable name for Item. """
        return "{0}".format(object.get_type().__str__())
        
    class Meta:
        model = Item
        fields = ('id', 'name', 'itype', 'amount', 'date_init', 'location', 'params')
                