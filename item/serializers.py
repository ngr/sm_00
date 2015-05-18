### Item Serializer ###
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

class ItemSerializer(serializers.ModelSerializer):
    """ Used to serialize Items for API. """
    name   = serializers.SerializerMethodField(read_only=True)
    amount = serializers.SerializerMethodField(read_only=True)
     
    def get_name(self, object):
        """ Return some readable name for Item. """
        return "{0}".format(object.get_type().__str__())

    def get_amount(self, object):
        """ Return amount in Item pile. """
        return object.amount
        
    class Meta:
        model = Item
        fields = ('id', 'name', 'itype', 'amount', 'location')

class ItemDetailSerializer(ItemSerializer):
    """ Used to serialize Items for API. """
    params = serializers.SerializerMethodField(read_only=True)

    def get_params(self, object):
        """ Get ItemDirectory params. """
        base_params_qs = object.itype.get_param().all()
        serializer = ItemParamSerializer(base_params_qs, many=True)
        return serializer.data

    class Meta:
        model = Item
        fields = ('id', 'name', 'itype', 'amount', 'date_init', 'location', 'params')
                