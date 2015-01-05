from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from task.models import Task
from task.tables import ActiveTaskTable

class ActiveTaskList(generic.View):
    def get(self, request):
        taq = Task.objects.filter(_date_finish__gte=timezone.now()).all()
        r = []
        for i in range(0, len(taq)):
            print(taq)
            r.append([taq,{'assignment_set': taq[i].assignment_set}])


        print(r)

#        tasks_active = ActiveTaskTable(r)
        tasks_active = ActiveTaskTable(taq)
#       print(taq.all()[0].assignment_set.all())

        tasks_to_retrieve = ActiveTaskTable(Task.objects.filter(_date_finish__lt=timezone.now(), _retrieved=0))
        tasks_all = ActiveTaskTable(Task.objects.all())
        
        result = {
                'tasks_active': tasks_active,
                'tasks_to_retrieve': tasks_to_retrieve,
                'tasks_all': tasks_all,
                }

        
        return render(request, 'task/task_list.html', result)


class TaskDetail(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)

#        print(kwargs)
#       self.region = get_object_or_404(Region, pk=kwargs['object'].pk)
#        print(self.region)
        print(self.get_object().id)
        context['assignments'] = self.get_object().assignment_set.all()
#       context['farming']   = self.region.get_farming_areas()

#       context['inhabitants'] = self.region.get_slaves(withdead=False)
        return context

# Create your views here.
