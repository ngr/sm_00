### Slave API Views ###
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from slave.models import Slave
from slave.serializers import SlaveSerializer, SlaveDetailSerializer

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
        except Item.DoesNotExist:
            return Response("Authorization error or wrong Slave id.",
                status=status.HTTP_404_NOT_FOUND)
        
        return Response(self.serializer_class(slave).data)      