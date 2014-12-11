from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from slave.models import Slave

class IndexView(generic.ListView):

    template_name = 'slave/index.html'
    context_object_name = 'slaves_list'

    def get_queryset(self):
        return Slave.objects.filter(
                date_birth__lte=timezone.now()
                ).order_by('-id')[:5]

class SlaveView(generic.DetailView):
    model = Slave
    template_name = 'slave/detail.html'
    def get_queryset(self):
        """ Exclude slaves not yet born """
        return Slave.objects.filter(date_birth__lte=timezone.now())

def make_happy(request, sid):
    p = get_object_or_404(Slave, pk=sid)
    p.happiness = request.POST['happiness']
    p.save()
    return HttpResponseRedirect(reverse('slave:results', args=(p.id,)))

class ResultsView(generic.DetailView):
    model = Slave
    template_name = 'slave/detail.html'

# Create your views here.
