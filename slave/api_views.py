### Slave API Views ###
from django.db.models import F, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import pagination

from slave.models import Slave
from slave.serializers import SlaveSerializer, SlaveDetailSerializer
from slave.helpers import filter_by_attribute, filter_by_location_region

class API_SlaveList(generics.ListAPIView):
    """ List Slaves. """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class   = SlaveSerializer

    def get_queryset(self):
        """ Return Slaves of the current user. """
            
    # Authorization check.
        # We assume later that slave_list is already
        # filtered with authorized slaves only so we may
        # simply add some more filters.    
        slave_list = Slave.objects.filter(owner=self.request.user)

    # Filter by valid attributes
        valid_params = ['location', 'sex']
        for attr in valid_params:
            if attr in self.request.query_params:
                slave_list = filter_by_attribute(slave_list,\
                    attribute_name=attr,\
                    attribute=self.request.query_params.get(attr))

    # Filter by Region
        if 'region' in self.request.query_params:
            slave_list = filter_by_location_region(slave_list, self.request.query_params.get('region'))
        
    # Filter free Slaves
        if 'free' in self.request.query_params:
            # FIXME! This looks quite shitty.
            # We compare the number of assignments to number of released ones.
            # If the numbers are equal - then nothing is currently running.
            # Unfortunately I couldn't yet filter by annotation of NON-released ones.
            slave_list = slave_list.annotate(assgns=Count('assignments')).\
                annotate(rel_assgns=Count('assignments__date_released')).\
                filter(assgns=F('rel_assgns'))

    # Order By
        # Should one day get the ordering from request.
        slave_list = slave_list.order_by('location', 'date_birth')
        
    # Paginate
        # FIXME The build in "LimitOffsetPagination" didn't work
        # Had to write directly in the view.
        if any(q for q in self.request.query_params if q in ['limit', 'offset']):
            if 'limit' in self.request.query_params:
                limit = int(self.request.query_params.get('limit'))
            offset = int(self.request.query_params.get('offset'))\
                if 'offset' in self.request.query_params else 0
            if 'limit' in locals():
                slave_list = slave_list[offset:limit+offset]
            else:
                slave_list = slave_list[offset:]

        return slave_list
    
    
    
class API_SlaveDetail(APIView):
    """ Slave Details. """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class   = SlaveDetailSerializer

    def get_object(self, pk):
        """ Get already authorized Item."""
        return Slave.objects.get(pk=pk, owner=self.request.user)

    def get(self, request, pk, format=None):
        # Get authorized Slave
        try:
            slave = self.get_object(pk)
        except Slave.DoesNotExist:
            return Response("Authorization error or wrong Slave id.",
                status=status.HTTP_404_NOT_FOUND)
        
        return Response(self.serializer_class(slave).data)      