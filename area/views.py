# AREA Views #
#from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponseRedirect, HttpResponseForbidden
#from django.core.urlresolvers import reverse
#from django.contrib.auth.decorators import login_required
#from django.views import generic
#from sm_00.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from area.models import Region, Location, LocationDirectory
from area.serializers import RegionSerializer, RegionDetailSerializer, LocationSerializer, LocationDetailSerializer, LocationDirectorySerializer

########
# RESTful API views.

class API_RegionList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegionSerializer

    def get_queryset(self):
        """ Return Regions of the current user. """
            
    # Authorization check.
        # We assume later that region_list is already
        # filtered with authorized regions only so we simply
        # add some more filters.
        region_list = Region.objects.filter(owner=self.request.user)

    # Paginate
        # FIXME The build in "LimitOffsetPagination" didn't work
        # Had to write directly in the view. NEED TO DRY THIS!
        if any(q for q in self.request.query_params if q in ['limit', 'offset']):
            if 'limit' in self.request.query_params:
                limit = int(self.request.query_params.get('limit'))
            offset = int(self.request.query_params.get('offset'))\
                if 'offset' in self.request.query_params else 0
            if 'limit' in locals():
                region_list = region_list[offset:limit+offset]
            else:
                region_list = region_list[offset:]
        
   
        return region_list

class API_LocationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LocationSerializer 

    def get_queryset(self):
        """ Return Locations of the current user. 
            You may specify Location in GET request. """
            
    # Authorization check.
        # We assume later that location_list is already
        # filtered with authorized locations only so we simply
        # add some more filters.
        location_list = Location.objects.filter(region__owner=self.request.user)

    # Region filtering.
        # There is filtering locations by Region available.
        if 'region' in self.request.query_params:
            try:
                location_list = location_list.filter(region=int(self.request.query_params['region']))
            except:
                pass
        
    # Paginate
        # FIXME The build in "LimitOffsetPagination" didn't work
        # Had to write directly in the view. NEED TO DRY THIS!
        if any(q for q in self.request.query_params if q in ['limit', 'offset']):
            if 'limit' in self.request.query_params:
                limit = int(self.request.query_params.get('limit'))
            offset = int(self.request.query_params.get('offset'))\
                if 'offset' in self.request.query_params else 0
            if 'limit' in locals():
                location_list = location_list[offset:limit+offset]
            else:
                location_list = location_list[offset:]        
        
        return location_list

class API_LocationDirectoryList(generics.ListAPIView):
    serializer_class = LocationDirectorySerializer 

    def get_queryset(self):
        """ Return all LocationDirectories. """
           
    # We now assume that all location designs are available to every player.
        location_directory_list = LocationDirectory.objects.all()
        
        return location_directory_list

class API_RegionDetail(APIView):
    """ Details of Region object. """
    # FIXME! Should DRY this. RetrieveAPIView makes it easy!
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegionDetailSerializer 
        
    def get_object(self, pk):
        """ Get already authorized Region."""
        region_object = Region.objects.get(pk=pk, owner=self.request.user)
        return region_object

    def get(self, request, pk, format=None):
        try:
            region = self.get_object(pk)
        except Region.DoesNotExist:
            return Response("Authorization error or wrong Region id.",
                status=status.HTTP_404_NOT_FOUND)
        
        return Response(self.serializer_class(region).data)
    
    def put(self, request, pk):
        """ We allow to modify only the name of the Region,
            or call built-in methods. """
    #   Get authorized Region to deal with.
        # Although user can try to specify a different 'pk' in his JSON,
        # everything should be OK and only the one from URL will be used.
        # Maybe check this possible security issue one day.
        try:
            region = self.get_object(pk)
        except Region.DoesNotExist:
            return Response("Authorization error or wrong Region id.",
                status=status.HTTP_403_FORBIDDEN)

        print(self.request.data)
        # We do not have any built-in methods now, so this is just a stub.
        return Response(self.serializer_class(region).data)
        
    
        
class API_LocationDetail(APIView):
    """ Details of Location object. """
    # FIXME! Should DRY this. RetrieveAPIView makes it easy!

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LocationDetailSerializer 

    def get_object(self, pk):
        """ Get already authorized Location."""
        return Location.objects.get(pk=pk, region__owner=self.request.user)

    def get(self, request, pk, format=None):
        try:
            location = self.get_object(pk)
        except Location.DoesNotExist:
            return Response("Authorization error or wrong Location id.",
                status=status.HTTP_404_NOT_FOUND)
        
        return Response(self.serializer_class(location).data)        
