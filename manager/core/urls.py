from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^playlist/$', views.playlist, name='playlist'),
    url(r'^song/$', views.song, name='song'),
)