# SLAVE VIEWS #

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django import forms

from oauth2_provider.views.generic import ProtectedResourceView

import urllib.request
import json
import codecs
import requests

from slave.models import Slave
from slave.forms import AssignToTaskForm
from area.models import Region

from sm_00.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'slave/index.html'
    context_object_name = 'slaves_list'
    paginate_by = 15 
    def get_queryset(self):
#        return Region.objects.all().get(pk=2).get_slaves()
        print(self.request.user)
        return Slave.objects.auth_get_slave(owner=self.request.user)
#       return Slave.objects.filter(
#               date_birth__lte=timezone.now()
#               ).order_by('-id')[:5]

class SlaveView(LoginRequiredMixin, generic.DetailView):
    model = Slave
    template_name = 'slave/detail.html'
    def get_queryset(self):
        """ Exclude slaves not yet born """
#        return Slave.objects.filter(date_birth__lte=timezone.now())
        return Slave.objects.auth_get_slave(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SlaveView, self).get_context_data(**kwargs)
        self.slave = get_object_or_404(Slave, pk=kwargs['object'].pk)
    
    # This is the form to assign Slave to any of available Tasks.
        # Hide slave field. This not for security, just design improvement.
        context['assign_form'] = AssignToTaskForm(initial={'slave': self.slave.id})
        context['assign_form'].fields['slave'].widget = forms.HiddenInput()
   
        # Add values for Task.
        
        if not self.request.session['access_token']:
        # FIXME Should automatically offer to relogin
            return context
#################        
        payload = {
                'format': 'json', 
                'running': '1',                
            }
        auth_header = {
                'Authorization': 'Bearer ' + self.request.session['access_token']
            }
        try:
            r = requests.get('http://aws00.grischenko.ru:8000/api/task/',
                headers=auth_header,
                params=payload)
            print ("Received JSON from Task App:", r.json())
        except:
            print("Error. Failed to get JSON from Task App.")
                
        # Add available tasks to context.
        context['assign_form'].fields['task'].choices = []
        for task in r.json():
            context['assign_form'].fields['task'].choices.append((task['id'], task['get_name_readable']))

        return context

def make_happy(request, sid):
    p = get_object_or_404(Slave, pk=sid)
    p.happiness = request.POST['happiness']
    p.save()
    return HttpResponseRedirect(reverse('slave:results', args=(p.id,)))

def set_skill(request, sid):
    p = get_object_or_404(Slave, pk=sid)
    p.add_skill_exp(int(request.POST['skill']), int(request.POST['exp']))
    return HttpResponseRedirect(reverse('slave:results', args=(p.id,)))

def assign_task(request, sid):
    form = AssignToTaskForm(request.POST)
    if form.is_valid():
        print("Form is OK")
        return HttpResponseRedirect(reverse('slave:detail', args=(form.cleaned_data['slave'],)))
    else:
        print("Error in Form")
        return HttpResponseRedirect(reverse('slave:results', args=(form.cleaned_data['slave'],)))

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Slave
    template_name = 'slave/detail.html'

##################

