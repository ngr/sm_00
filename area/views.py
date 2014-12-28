from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from area.models import Region, Location


class RegionList(generic.ListView):
#   context_object_name = 'available_regions'
#   template_name = 'area/index.html'
    model = Region

#   def get_queryset(self):
#       """ Return list of available Regions """
#       return Region.objects.all()

class RegionDetail(generic.DetailView):
    model = Region

    def get_context_data(self, **kwargs):
        context = super(RegionDetail, self).get_context_data(**kwargs)

#        print(kwargs)
        self.region = get_object_or_404(Region, pk=kwargs['object'].pk)
#        print(self.region)
        context['housing'] = self.region.get_housing() 
        context['farming']   = self.region.get_farming_areas()

        context['inhabitants'] = self.region.get_slaves(withdead=False)
        return context

""" def RegionView(request, region_id):
    region = Region.objects.get(pk=region_id)
    region_locations = region.get_locations()
    print(region_locations)
    context = {'region': region}
    context['locations'] = region_locations

    return render(request, 'area/detail.html', context)
"""


# Create your views here.
