# FIXME 
# Should clean a lot of these includes!
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views import generic
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from task.tables import ActiveTaskTable

from slave.logic import AssignmentError, TaskError
from task.models import Task, Assignment
from area.models import Region

from sm_00.mixins import LoginRequiredMixin

class RegionTaskList(LoginRequiredMixin, generic.View):
    """ Authorized list of tasks in the selected Region. """
    def get(self, request, region):
        """ GET method processor. """
        
      # We find the region instance here. NOT IN TASK CLASS! 
      # Should think how to make it better later.
        if not int(region):
            print(region)
            return HttpResponseForbidden() 
        
        r = Region.objects.get(pk=region)
        tasks_query = Task.objects.auth_get_running_available(self.request.user, region=r).\
            filter(_date_finish__gte=timezone.now()).all()
        
      # Add assignments to result
        r = []
        for i in range(0, len(tasks_query)):
            r.append([tasks_query,{'assignments': tasks_query[i].assignments}])

        result = {
            'tasks_available': tasks_query,
            }
        return render(request, 'task/region_running_task_list.html', result)

class ActiveTaskList(LoginRequiredMixin, generic.View):
    def get(self, request):
        taq = Task.objects.auth_get_task(self.request.user).filter(_date_finish__gte=timezone.now()).all()
        r = []
        for i in range(0, len(taq)):
            print(taq)
            r.append([taq,{'assignments': taq[i].assignments}])

        
        print(r)

#        tasks_active = ActiveTaskTable(r)
        tasks_active = ActiveTaskTable(taq)
#       print(taq.all()[0].assignments.all())

        tasks_to_retrieve = ActiveTaskTable(Task.objects.auth_get_task(self.request.user).filter(_date_finish__lt=timezone.now(), _retrieved=0))
        tasks_all = ActiveTaskTable(Task.objects.auth_get_task(self.request.user).order_by('-id')[:15:1])
#        RequestConfig(request, paginate={"per_page": 10}).configure(tasks_all)

        result = {
                'tasks_active': tasks_active,
                'tasks_to_retrieve': tasks_to_retrieve,
                'tasks_all': tasks_all,
                }

        
        return render(request, 'task/task_list.html', result)

class TaskDetail(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        self.task = get_object_or_404(Task, pk=kwargs['object'].pk)

# Authorization check!
        if not self.task.auth_allowed(self.request.user):
            self.task = None
            return HttpResponseForbidden()

        context['assignments'] = self.get_object().assignments.all()
        return context

########
# Below come new cool RESTful API views.
#