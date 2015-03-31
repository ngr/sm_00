from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from task import views

urlpatterns = patterns('',
        url(r'^$', views.ActiveTaskList.as_view(), name='index'),
        url(r'^region/(\d+)/$', views.RegionTaskList.as_view(), name='region'),
        url(r'^(?P<pk>\d+)/$', views.TaskDetail.as_view(), name='task_detail'),

#        url(r'^api/$', views.API_TaskList.as_view(), name='index'),        
#        url(r'^assignment/$', views.API_AssignmentList.as_view()),
#        url(r'^assignment/(?P<pk>[0-9]+)/$', views.AssignmentDetail.as_view()),
        

    )
urlpatterns = format_suffix_patterns(urlpatterns)
