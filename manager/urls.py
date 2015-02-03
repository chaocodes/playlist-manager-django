from django.conf.urls import patterns, include, url
from django.contrib import admin

from .core.urls import urlpatterns as core_urls
from .userprofile.urls import urlpatterns as userprofile_urls
from .playlist.urls import urlpatterns as playlist_urls
from .song.urls import urlpatterns as song_urls
from .search.urls import urlpatterns as search_urls

urlpatterns = patterns('',
    url(r'^', include(core_urls, namespace='core')),
    url(r'^user/', include(userprofile_urls, namespace='userprofile')),
    url(r'^user/(?P<user_id>\d+)/playlist/', include(playlist_urls, namespace='playlist')),
    url(r'^user/(?P<user_id>\d+)/playlist/(?P<playlist_id>\d+)/song/', include(song_urls, namespace='song')),
    url(r'^search/', include(search_urls, namespace='search')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)