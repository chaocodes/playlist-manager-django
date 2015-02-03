from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.users, name='all'),
    url(r'^(?P<user_id>\d+)/$', views.user, name='one'),
    url(r'^(?P<user_id>\d+)/edit/$', views.edit_view, name='edit'),
)