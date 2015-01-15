from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

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
        context['assign_form'] = AssignToTaskForm()
        return context

def make_happy(request, sid):
    p = get_object_or_404(Slave, pk=sid)
    p.happiness = request.POST['happiness']
    p.save()
    return HttpResponseRedirect(reverse('slave:results', args=(p.id,)))

def set_skill(request, sid):
    p = get_object_or_404(Slave, pk=sid)
    p.set_skill(request.POST['skill'], request.POST['exp'])
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

