from django.forms import widgets
from rest_framework import serializers
from item.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', '_name', '_itype', '_amount', '_date_init', '_warehouse')
