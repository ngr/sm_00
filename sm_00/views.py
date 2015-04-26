# SM_00 views #
from base64 import b64encode
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.views import generic
from django.utils import timezone
from slave.models import Slave
from area.models import Region
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import generics

from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
import requests
from requests_oauthlib import OAuth1

from sm_00.serializers import UserSerializer
from django.contrib.auth.models import User

def SlaveMasterLogin(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
      # Authentication is successful
        if user is not None:
            if user.is_active:
              # Login in Django auth
                login(request, user)
        # Generate Token
              # I tried to use several libs to control tokens. They sucked.
              # So here is a MANUAL temporary token retrieve method.
                application_id = "4ci299zGdWnwTWmYlwvk13vsAro60jkoVe9bztz6"
                application_secret = "nf7WsWxuB0YW1MqjcryHIwRnegU6KnYCaGGnYyehEs6wb3MVXcndPrBjT0xPRBVAD0XNzwX5RX3LBZ7X76BKan90jAbpFQdgpsaP3zLFNFcBJbxWcy1bO9JnQRecgOHW"
                token_url = 'http://aws00.grischenko.ru:8000/o/token/'   
              
              # This is authorization for new token generation.
              # FIXME! Secret should be kept somewhere else!
              # Here is an UGLY trick to convert str to base64 and use it for auth.
              # As long as we use bytes, the first 2 symbols are: b'
                code = str(b64encode((application_id + ":" + application_secret).encode('ascii')))[2:]
                headers = {'Authorization': 'Basic ' + code}
                payload = {
                    'grant_type': 'password',
                    'username': username,
                    'password': password
                }
                r = requests.post(token_url, headers=headers, data=payload)
                response_json = r.json()
                #print(response_json)
              # Save tokens to session
                request.session['access_token'] = response_json['access_token']
                request.session['refresh_token'] = response_json['refresh_token']

        # Final redirect
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect('/')
                   
    # In case we do not have a POST request we show the login Form.    
    return render_to_response('sm_00/login.html', context_instance=RequestContext(request))

class APIEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        auth_header = {
             #   'Authorization': 'Bearer ' + self.request.session['api_token']
            }

        result = "Successfully authenticated as " + str(request.user) +"\n"
        result += "Got a token: " + str(request.session['auth_token']) +"\n"
        result += "Got a refresh token: " + str(request.session['refresh_token']) +"\n"
        return HttpResponse(result, status=200)
        
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
<<<<<<< HEAD
        'slaves': reverse('api:slave-list', request=request, format=format),
=======
>>>>>>> 96dec8ae7fccff2913e8ca5c25a572e6de2d48c2
        'items': reverse('api:item-list', request=request, format=format),
        'tasks': reverse('api:task-list', request=request, format=format),
        'assignments': reverse('api:assignment-list', request=request, format=format),
        'regions': reverse('api:region-list', request=request, format=format),
        'locations': reverse('api:location-list', request=request, format=format),
        'locationdirectories': reverse('api:locationdirectory-list', request=request, format=format),
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
 
