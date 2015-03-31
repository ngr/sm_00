from django.conf.urls import patterns, include, url
from django.contrib import admin
from sm_00 import views
from task import views as task_views

urlpatterns = patterns('',
    # Examples:
 #   url(r'^$', views.IndexView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.api_root),
    url(r'^task/$', task_views.API_TaskList.as_view(), name='task-list'),            
    url(r'^task/(?P<pk>[0-9]+)/$', task_views.API_TaskDetail.as_view(), name='task-detail'),
    
    url(r'^assignment/$', task_views.API_AssignmentList.as_view(), name='assignment-list'),
    url(r'^assignment/(?P<pk>[0-9]+)/$', task_views.API_AssignmentDetail.as_view(), name='assignment-detail'),


)
