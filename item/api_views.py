from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from item.models import Item
from item.serializers import ItemSerializer

########
# RESTful API views.

class API_ItemList(generics.ListAPIView):
    """ List all items. """
    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
