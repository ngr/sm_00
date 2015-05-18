from django.db.models import Q
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from item.models import Item, ItemDirectory
from item.serializers import ItemSerializer, ItemDetailSerializer

########
# RESTful API views.

class API_ItemList(generics.ListAPIView):
    """ List Items. """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class   = ItemSerializer

    def get_queryset(self):
        """ Return Items of the current user. """
            
    # Authorization check.
        # We assume later that item_list is already
        # filtered with authorized items only so we may
        # simply add some more filters.    
        item_list = Item.objects.filter(location__region__owner=self.request.user)

    # Filter by location
        if 'location' in self.request.query_params:
            # Make a list of requested values in location attribute
            # May be a plain csv or list/tuple styled csv
            location_list = [x.strip(' []()') for x in self.request.query_params.get('location').split(',')]
            
            # Now iterate through the list to check types
            validated_location_list = [] # Used for final attributes of this filter
            for i in location_list:
                # We do not allow other types than numeric ID of location.
                if i.isnumeric():
                    validated_location_list.append(i)
            item_list = item_list.filter(location__in=validated_location_list)
        
    # Filter by itype
        if 'itype' in self.request.query_params:
            itype_list = [x.strip(' []()') for x in self.request.query_params.get('itype').split(',')]
            
            temp_itype_list = []
            for i in itype_list:
                if i.isnumeric():
                    temp_itype_list.append(i)
                else:
                    itype_q = ItemDirectory.objects.filter(name=i)
                    if itype_q.count() > 0:
                        temp_itype_list.append(itype_q.first())
            itype_list = temp_itype_list
            item_list = item_list.filter(itype__in=itype_list)
            
    # FIXME Add accumulation here
        if 'region' in self.request.query_params:
            item_list = item_list.annotate(Sum('amount'))
        

    # Paginate
        # FIXME The build in "LimitOffsetPagination" didn't work
        # Had to write directly in the view. NEED TO DRY THIS!
        if any(q for q in self.request.query_params if q in ['limit', 'offset']):
            if 'limit' in self.request.query_params:
                limit = int(self.request.query_params.get('limit'))
            offset = int(self.request.query_params.get('offset'))\
                if 'offset' in self.request.query_params else 0
            if 'limit' in locals():
                item_list = item_list[offset:limit+offset]
            else:
                item_list = item_list[offset:]
                    
        return item_list

class API_ItemDetail(APIView):
    """ List Items. """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class   = ItemDetailSerializer

    def get_object(self, pk):
        """ Get already authorized Item."""
        return Item.objects.get(pk=pk, location__region__owner=self.request.user)

    def get(self, request, pk, format=None):
        # Get authorized Item
        try:
            item = self.get_object(pk)
        except Item.DoesNotExist:
            return Response("Authorization error or wrong Item id.",
                status=status.HTTP_404_NOT_FOUND)
        
        return Response(self.serializer_class(item).data)        
