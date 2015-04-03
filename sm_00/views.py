from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.views import generic
from django.utils import timezone
from slave.models import Slave
from area.models import Region
from django.contrib.auth.views import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import generics

from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required

from sm_00.serializers import UserSerializer
from django.contrib.auth.models import User

@login_required()
def secret_page(request, *args, **kwargs):
    result = "Successfully authenticated as " + str(request.user) +"\n"
    return HttpResponse(result, status=200)

class APIEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'task': reverse('api:task-list', request=request, format=format),
        'assignment': reverse('api:assignment-list', request=request, format=format)
    })


class LogoutView(RedirectView):
    
    pass

class IndexView(TemplateView):

    template_name = 'sm_00/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
#print("InxexView",context['user'])
        return context

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
