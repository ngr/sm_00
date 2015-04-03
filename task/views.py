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

from task.serializers import TaskSerializer, AssignmentSerializer
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
class API_TaskList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer 

    def get_queryset(self):
        """ Return tasks of the current user. 
            You may specify Task or Slave in GET request. """
            
    # Authorization check.
        # We assume later that task_list is already
        # filtered with authorized tasks only so we simply
        # add some more filters.
        task_list = Task.objects.filter(owner=self.request.user)

    # Now, when we filter the queryset all filters are not
    # critical, so if we can't interpret the given param obviously
    # we do not raise errors but simply skip the filter.
        
    # Filtering running tasks.
        # The default is to show all Tasks.
        # You can add 'running' param to filter only running Tasks,
        # Or set it to False to get already retrieved ones.
        if 'running' in self.request.query_params:
            running_request = self.request.query_params.get('running')
            if running_request in ('True', 'true', '1', 'yes', ''):
                task_list = task_list.filter(_retrieved=False)
            elif running_request in ('False', 'false', '0', 'no'):
                task_list = task_list.filter(_retrieved=True)
                
    # Filtering by Location.
        if 'location' in self.request.query_params:
            try:
                task_list = task_list.filter(location=int(self.request.query_params['location']))
            except:
                pass

    # Filtering by Region.
        if 'region' in self.request.query_params:
            try:
                task_list = task_list.filter(location__region=int(self.request.query_params['region']))
            except:
                pass
                
    # Filtering by Type.
        if 'type' in self.request.query_params:
            type = self.request.query_params.get('type')
            # ADDON WANTED  
            # Maybe should make string search for types available here.
            if type.isnumeric():
                try:
                    task_list = task_list.filter(type=type)
                except:
                    pass

        return task_list

    def post(self, request):
        """ Create a new task. """

    # Authorize current user for requested Task.
        print("data: {0},  request: {1}".format(request.data.get('owner'), request.user.id))
        if int(request.data.get('owner')) != request.user.id:
            return Response("Authorization error for this task.",
                status=status.HTTP_403_FORBIDDEN)

    # Serialize incoming data as a new Task.
        serializer = TaskSerializer(data=request.data)

    # Validate data
        # Gameplay rules and more security issues 
        # are processed in serializer validators.
        if serializer.is_valid(request):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class API_TaskDetail(APIView):
#    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        """ Get already authorized object."""
        return Task.objects.get(pk=pk, owner=self.request.user)
    
    def get(self, request, pk, format=None):
        try:
            task = self.get_object(pk)
        except Task.DoesNotExist:
            return Response("Authorization error or wrong Task id.",
                status=status.HTTP_403_FORBIDDEN)
 
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ PUT method is used to call built-in METHODS on existing Task object. """
        
    #   Get authorized Task to deal with.
        # Although user can try to specify a different 'pk' in his JSON,
        # everything should be OK and only the one from URL will be used.
        # Maybe check this possible security issue one day.
        try:
            task = self.get_object(pk)
        except Task.DoesNotExist:
            return Response("Authorization error or wrong Task id.",
                status=status.HTTP_403_FORBIDDEN)

        print(self.request.data)     
        
        # There are currently only several actions available here,
        # so I didn't make any cool switch here.

        # Process release action
        if self.request.data.get('action') == 'retrieve':
            try:
                result = task.retrieve()
            except Exception as current_exception:
            # Different Response Codes are used.
                if str(current_exception) == "Task was already retrieved.":
                # If the Task was already successfully retrieved - 409.
                    return Response("Error. Task was already retrieved.",
                        status=status.HTTP_409_CONFLICT)
                elif str(current_exception) == "Task is not finished yet.":
                    return Response("Error. Task is not finished yet.",
                        status=status.HTTP_409_CONFLICT)
                else:
                # Otherwise - 400
                    return Response("Error. While retrieving task.",
                        status=status.HTTP_400_BAD_REQUEST)
                       
            # We use asynchronous response "for the better future",
            # while actually we have already tried to retrieve the Task.
            if result:
                return Response("Success. Task was retrieved.", 
                    status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Error. While retrieving task.",
                    status=status.HTTP_400_BAD_REQUEST)
           
        # If smth went wrong with validation we return the errors in HTTP status 400.
        return Response("Error. No valid action specified.",
            status=status.HTTP_400_BAD_REQUEST)


class API_AssignmentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        """ Return assignments of the current user. 
            You may specify Task or Slave in GET request. """
        
    # Authorization check
        # We assume same as with task_list.
        # See comments in class API_TaskList->get_queryset()
        assignment_list = Assignment.objects.filter(task__owner=self.request.user)

#        print(self.request.query_params)
    # Filtering running Assignments.
        # The default is to show all Assignments.
        # You can add 'running' param to filter only non-finished ones,
        # Or set it to False to get already released ones.
        if 'running' in self.request.query_params:
            running_request = self.request.query_params.get('running')
            if running_request in ('True', 'true', '1', 'yes', ''):
                print("Filter running Assignments")
                assignment_list = assignment_list.filter(date_released__isnull=True)
            elif running_request in ('False', 'false', '0', 'no'):
                print("Filter released Assignments")
                assignment_list = assignment_list.filter(date_released__isnull=True)

    # Filtering by Task
        if 'task' in self.request.query_params:
            try:
                assignment_list = assignment_list.filter(task=int(self.request.query_params['task']))
            except:
                pass

    # Filtering by Slave
        if 'slave' in self.request.query_params:
            try:
                assignment_list = assignment_list.filter(slave=int(self.request.query_params['slave']))
            except:
                pass
         
        return assignment_list

    def post(self, request, format=None):
        """ Save new assignment. """
        
    # Check if the user has rights.
        # I expect that this extra select query by Task PK 
        # will not add extra load to DB. I do not really know 
        # RESTful API good enough at the moment to check more effectively.
        task = Task.objects.get(pk=request.data['task'])
        if task.get_owner() != request.user:
            return Response("Authorization error for this task.",
                status=status.HTTP_403_FORBIDDEN)
      
    # Serialize incoming data as a new assignment.
        serializer = AssignmentSerializer(data=request.data)
        
    # Validate data
        # Gameplay rules and more security issues 
        # are processed in serializer validators.
        if serializer.is_valid(request):
            serializer.save()
            # Resave Task to automatically update estimated finish.
            task.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class API_AssignmentDetail(APIView):
    def get_object(self, pk):
        """ Get already authorized object."""
        return Assignment.objects.get(pk=pk, task__owner=self.request.user)

    def get(self, request, pk, format=None):
        try:
            assignment = self.get_object(pk)
        except Assignment.DoesNotExist:
            return Response("Authorization error or wrong Assignment id.",
                status=status.HTTP_403_FORBIDDEN)
 
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ PUT method is used to call built-in METHODS on existing Assignment object. """
        
    #   Get authorized Assignment to deal with.
        # Although user can try to specify a different 'pk' in his JSON,
        # everything should be OK and only the one from URL will be used.
        # Maybe check this possible security issue one day.
        try:
            assignment = self.get_object(pk)
        except Assignment.DoesNotExist:
            return Response("Authorization error or wrong Assignment id.",
                status=status.HTTP_403_FORBIDDEN)

#        print(self.request.data)     
        
        # There are currently only several actions available here,
        # so I didn't make any cool switch here.

        # Process release action
        if self.request.data.get('action') == 'release':
            result = assignment.release()
            
            # We use asynchronous response "for the better future",
            # while actually we have already released the Assignment.
            if result:
                # Resave Task to automatically update estimated finish.
                assignment.task.save()
                return Response("Success. Assignment was released.", 
                    status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Error. Assignment was already released.",
                    status=status.HTTP_409_CONFLICT)
           
        # If smth went wrong with validation we return the errors in HTTP status 400.
        return Response("Error. No valid action specified.",
            status=status.HTTP_400_BAD_REQUEST)