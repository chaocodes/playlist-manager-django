from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.playlists, name='all'),
    url(r'^create/$', views.create_view, name='create'),
    url(r'^(?P<playlist_id>\d+)/$', views.playlist, name='one'),
    url(r'^(?P<playlist_id>\d+)/edit/$', views.edit_view, name='edit'),
)