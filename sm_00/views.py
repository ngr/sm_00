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


#class Navigation(generic.View):
#    template_name = 'sm_00/navigation.html'
#    print("LOAD NAV")
#    object = ['slave', 'task', 'skill']
#    def get(self, request, *args, **kwargs):
#       return super(Navigation, self).get(request, *args, **kwargs)

class LogoutView(RedirectView):
    
    pass

class IndexView(TemplateView):

    template_name = 'sm_00/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
#print("InxexView",context['user'])
        return context
#    def get(self, request):

#        pass
#    context_object_name = 'slaves_list'

#    def get_queryset(self):
#        return ''
#        return Region.objects.all().get(pk=2).get_slaves()





# Create your views here.
