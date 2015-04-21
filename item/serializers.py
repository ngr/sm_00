from django.forms import widgets
from rest_framework import serializers
from item.models import Item, ItemBaseParam, Item


class ItemParamSerializer(serializers.ModelSerializer):
    name    = serializers.CharField()
    value   = serializers.CharField()
    class Meta:
        model  = ItemBaseParam
        fields = ('name', 'value')

class ItemSerializer(serializers.ModelSerializer):

    def get_params(self, object):
        """ Get ItemDirectory params. """
        base_params_qs = object.itype.get_param().all()
        print(base_params_qs)
    
        serializer = ItemParamSerializer(base_params_qs, many=True)
        print(serializer.data)
        return serializer.data
        
    params = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Item
        fields = ('id', 'itype', 'amount', 'date_init', 'location', 'params')
        