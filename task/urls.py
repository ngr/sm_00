from django.conf.urls import patterns, url

from task import views

urlpatterns = patterns('',
        url(r'^$', views.ActiveTaskList.as_view(), name='index'),
        url(r'^(?P<pk>\d+)/$', views.TaskDetail.as_view(), name='task_detail'),
#        url(r'^(\d+)/', views.TaskDetail.as_view(), name='task_detail'),

    )

