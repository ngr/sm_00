from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views import generic
from django.utils import timezone
#from django_tables2.utils import RequestConfig 

from task.models import Task
from task.tables import ActiveTaskTable

from sm_00.mixins import LoginRequiredMixin

class ActiveTaskList(LoginRequiredMixin, generic.View):
    def get(self, request):
        taq = Task.objects.auth_get_task(self.request.user).filter(_date_finish__gte=timezone.now()).all()
        r = []
        for i in range(0, len(taq)):
            print(taq)
            r.append([taq,{'assignment_set': taq[i].assignment_set}])

        
        print(r)

#        tasks_active = ActiveTaskTable(r)
        tasks_active = ActiveTaskTable(taq)
#       print(taq.all()[0].assignment_set.all())

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

        context['assignments'] = self.get_object().assignment_set.all()
        return context

