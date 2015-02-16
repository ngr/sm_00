from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic

from area.models import Region, Location

from sm_00.mixins import LoginRequiredMixin


class RegionList(LoginRequiredMixin, generic.ListView):
#   context_object_name = 'available_regions'
#   template_name = 'area/index.html'
    model = Region


    def get_queryset(self):
        """ Return list of available Regions """
        print(self.request.user)
        return Region.objects.auth_get_region(owner=self.request.user)

class RegionDetail(LoginRequiredMixin, generic.DetailView):
    model = Region

    def get_context_data(self, **kwargs):
        context = super(RegionDetail, self).get_context_data(**kwargs)
        self.region = get_object_or_404(Region, pk=kwargs['object'].pk)
# Authorization check!
        if not self.region.auth_allowed(self.request.user):
            self.region = None
            return HttpResponseForbidden()

        context['housing'] = self.region.get_housing() 
        context['farming']   = self.region.get_farming_areas()
        context['inhabitants'] = self.region.get_slaves(withdead=False)

        context['items'] = self.region.get_item_list()
        return context


# Create your views here.
