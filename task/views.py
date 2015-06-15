### Task API Views ###
from django.db.models import Q, Count

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from braces.views import CsrfExemptMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from slave.logic import AssignmentError, TaskError
from task.serializers import TaskSerializer, TaskDetailSerializer,\
    AssignmentSerializer, TaskDirectorySerializer
from task.models import Task, Assignment, TaskDirectory
from area.models import Region, LocationType
from slave.models import Slave

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
    
    # Filtering only available for given Slave
        if 'slave' in self.request.query_params:
            slave = self.request.query_params.get('slave')
            if slave.isnumeric():
                slave = Slave.objects.get(pk=slave)
            # Check permission
                if not slave.get_owner() == self.request.user:
                    print("Auth Error")
                    return []
            # Check skills. If Task Primary skill is available then OK.
                #print(slave.skills.all().values('skill'))
                task_list = task_list.filter(type__primary_skill__in=slave.skills.all().values('skill')).all()
            # Check Region
                task_list = task_list.filter(location__region=slave.location.region).all()

    # Order by assignments
        if 'orderBy' in self.request.query_params:
            order = self.request.query_params.get('orderBy')
        # First we order by number of assignments
            if 'assignments' in order:
                task_list = task_list.annotate(num_assignments=Count('assignments')).order_by('num_assignments')
        # Then by estimated date finish.            
            if 'date_finish' in order:
                task_list = task_list.order_by('date_finish')
            

    # Paginate
        # FIXME The build in "LimitOffsetPagination" didn't work
        # Had to write directly in the view.
        if any(q for q in self.request.query_params if q in ['limit', 'offset']):
            if 'limit' in self.request.query_params:
                limit = int(self.request.query_params.get('limit'))
            offset = int(self.request.query_params.get('offset'))\
                if 'offset' in self.request.query_params else 0
            if 'limit' in locals():
                task_list = task_list[offset:limit+offset]
            else:
                task_list = task_list[offset:]        

        return task_list

    def post(self, request):
        """ Create a new task. """

    # Authorize current user for requested Task.
        print("data: {0},  request: {1}".format(request.data, request.user.id))
        if int(request.data.get('owner')) != request.user.id:
            return Response("Authorization error for this task.",
                status=status.HTTP_403_FORBIDDEN)

    # Serialize incoming data as a new Task.
    # Important to use this one, as validators are in Detailed serializer only.
        serializer = TaskDetailSerializer(data=request.data)

    # Validate data
        # Gameplay rules and more security issues 
        # are processed in serializer validators.
        if serializer.is_valid(request):
            try:
                serializer.save()
            except Exception as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
                
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
 
        serializer = TaskDetailSerializer(task)
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
        # This action simply updates the auto fields on save()
        elif self.request.data.get('action') == 'update':
            try:
                result = task.save()
                return Response("Success. Task was updated.", 
                    status=status.HTTP_202_ACCEPTED)
            except:
                return Response("Error. While updating task.",
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

    # Paginate
        # FIXME The build in "LimitOffsetPagination" didn't work
        # Had to write directly in the view.
        if any(q for q in self.request.query_params if q in ['limit', 'offset']):
            if 'limit' in self.request.query_params:
                limit = int(self.request.query_params.get('limit'))
            offset = int(self.request.query_params.get('offset'))\
                if 'offset' in self.request.query_params else 0
            if 'limit' in locals():
                assignment_list = assignment_list[offset:limit+offset]
            else:
                assignment_list = assignment_list[offset:]        

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

class API_TaskWorkflowList(generics.ListAPIView):
    """ Listing TaskDirectory items for forms. """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskDirectorySerializer

    def get_queryset(self):
        """ Return available task workflow list. """
        task_workflow_list = TaskDirectory.objects.all()
    
    # Filter by specific Global Location Type.
        if 'location_type' in self.request.query_params:
            q_location = self.request.query_params.get('location_type')
            if not q_location.isnumeric():
                q_location = LocationType.objects.filter(name__exact=q_location.title()).first()
            task_workflow_list = task_workflow_list.filter(location_type=q_location)

        return task_workflow_list
    