from django.forms import widgets
from rest_framework import serializers
from item.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'itype', 'amount', 'date_init', 'location')
