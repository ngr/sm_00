from django.conf.urls import patterns, url

from area import views

urlpatterns = patterns('',
        url(r'^$', views.RegionList.as_view(), name='index'),
        url(r'^(?P<pk>\d+)/$', views.RegionDetail.as_view(), name='detail'),
    )

