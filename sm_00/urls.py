from django.conf.urls import patterns, include, url
from django.contrib import admin
from sm_00 import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.IndexView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^slave/', include('slave.urls', namespace='slave')),
    url(r'^area/', include('area.urls', namespace='area')),
    url(r'^task/', include('task.urls', namespace='task')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^talk/', include('talk.urls', namespace='talk')),
    url(r'^item/', include('item.urls', namespace='item')),

    url(r'^api/', include('sm_00.apiurls', namespace='api')),
    url(r'^a/hello', views.APIEndpoint.as_view()),  # and also a resource server!
    url(r'^secret$', 'sm_00.views.secret_page', name='secret'),

    
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),


)
