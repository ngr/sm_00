from django.conf.urls import patterns, url

from slave import views

urlpatterns = patterns('',
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^detail/(?P<pk>\d+)/$', views.SlaveView.as_view(), name='detail'),
        url(r'^detail/(?P<pk>\d+)/results$', views.ResultsView.as_view(), name='results'),
        url(r'^detail/(?P<sid>\d+)/make_happy$', views.make_happy, name='make_happy'),
        url(r'^detail/(?P<sid>\d+)/set_skill$', views.set_skill, name='set_skill'),
        url(r'^detail/(?P<sid>\d+)/assign_task$', views.assign_task, name='assign_task'),
#        url(r'^detail/\d+/create_post/$', views.create_post, name='create_post'),


)

