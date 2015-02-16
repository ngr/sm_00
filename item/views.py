from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from item.models import Item
from item.serializers import ItemSerializer


class ItemList(APIView):
    """ List all items or create new """
    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)



