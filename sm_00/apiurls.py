from django.conf.urls import patterns, include, url
from django.contrib import admin
from sm_00 import views
from task import views as task_views
from area import views as area_views
from item import api_views as item_views

urlpatterns = patterns('',
    # Examples:
 #   url(r'^$', views.IndexView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.api_root),

    url(r'^items/$', item_views.API_ItemList.as_view(), name='item-list'),            

    url(r'^task/$', task_views.API_TaskList.as_view(), name='task-list'),            
    url(r'^task/(?P<pk>[0-9]+)/$', task_views.API_TaskDetail.as_view(), name='task-detail'),
    
    url(r'^assignment/$', task_views.API_AssignmentList.as_view(), name='assignment-list'),
    url(r'^assignment/(?P<pk>[0-9]+)/$', task_views.API_AssignmentDetail.as_view(), name='assignment-detail'),

    url(r'^regions/$', area_views.API_RegionList.as_view(), name='region-list'),            
    url(r'^locations/$', area_views.API_LocationList.as_view(), name='location-list'),            
    url(r'^locationdirectories/$', area_views.API_LocationDirectoryList.as_view(), name='locationdirectory-list'),
    
    url(r'^region/(?P<pk>[0-9]+)/$', area_views.API_RegionDetail.as_view(), name='region-detail'),
    url(r'^location/(?P<pk>[0-9]+)/$', area_views.API_LocationDetail.as_view(), name='location-detail'),

)
