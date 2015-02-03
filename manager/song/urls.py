from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.songs, name='all'),
    url(r'^create/$', views.create_view, name='create'),
    url(r'^(?P<song_id>\d+)/$', views.song, name='one'),
    url(r'^(?P<song_id>\d+)/edit/$', views.edit_view, name='edit'),
)