from django.conf.urls import patterns, url
from item import views

urlpatterns = patterns('',
        url(r'^$', views.ItemList.as_view(), name='index'),
    )



