from django.conf.urls import patterns, url

from slave import views

urlpatterns = patterns('',
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^detail/(?P<pk>\d+)/$', views.SlaveView.as_view(), name='detail'),
        url(r'^detail/(?P<pk>\d+)/results$', views.ResultsView.as_view(), name='results'),
        url(r'^detail/(?P<sid>\d+)/make_happy$', views.make_happy, name='make_happy'),

)

