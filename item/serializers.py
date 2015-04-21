from django.forms import widgets
from rest_framework import serializers
from item.models import Item, ItemParam, Item


class ItemParamSerializer(serializers.ModelSerializer):
    name    = serializers.CharField()
    value   = serializers.CharField()
    class Meta:
        model  = ItemParam
        fields = ('name', 'value')

class ItemSerializer(serializers.ModelSerializer):

    def get_base_params(self, object):
        """ Accumulate Item-specific and Directory params. """
        base_params_qs = object.itype.get_param().all()
        specific_params_qs = object.get_param().all()
        print(base_params_qs)
    
        serializer = ItemParamSerializer(base_params_qs, many=True)
        print(serializer.data)
        return serializer.data
        
    params = ItemParamSerializer(many=True, read_only=True)
    base_params = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Item
        fields = ('id', 'itype', 'amount', 'date_init', 'location', 'params', 'base_params')
        