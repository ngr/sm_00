from django.conf.urls import patterns, include, url
from django.contrib import admin
from sm_00 import views
from task import views as task_views
from area import views as area_views
from item import api_views as item_views
from slave import api_views as slave_views

urlpatterns = patterns('',
    # Examples:
 #   url(r'^$', views.IndexView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.api_root),

    url(r'^slaves/$', slave_views.API_SlaveList.as_view(), name='slave-list'),            
    url(r'^slave/(?P<pk>[0-9]+)/$', slave_views.API_SlaveDetail.as_view(), name='slave-detail'),

    url(r'^items/$', item_views.API_ItemList.as_view(), name='item-list'),            
    url(r'^item/(?P<pk>[0-9]+)/$', item_views.API_ItemDetail.as_view(), name='item-detail'),

    url(r'^tasks/$', task_views.API_TaskList.as_view(), name='task-list'),            
    url(r'^task/(?P<pk>[0-9]+)/$', task_views.API_TaskDetail.as_view(), name='task-detail'),
    
    url(r'^assignments/$', task_views.API_AssignmentList.as_view(), name='assignment-list'),
    url(r'^assignment/(?P<pk>[0-9]+)/$', task_views.API_AssignmentDetail.as_view(), name='assignment-detail'),

    url(r'^regions/$', area_views.API_RegionList.as_view(), name='region-list'),            
    url(r'^region/(?P<pk>[0-9]+)/$', area_views.API_RegionDetail.as_view(), name='region-detail'),

    url(r'^locations/$', area_views.API_LocationList.as_view(), name='location-list'),            
    url(r'^location/(?P<pk>[0-9]+)/$', area_views.API_LocationDetail.as_view(), name='location-detail'),

    url(r'^locationdirectories/$', area_views.API_LocationDirectoryList.as_view(), name='locationdirectory-list'),
    

)
