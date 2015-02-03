from django.shortcuts import render

from manager.playlist.models import Playlist
from manager.song.models import Song

def index(request):
    data = {
        'playlists': Playlist.objects.order_by('-created_at')[:10],
        'songs': Song.objects.order_by('-created_at')[:10],
    }
    return render(request, 'core/home.html', data)

def playlist(request):
    data = {
        'playlists': Playlist.objects.order_by('-created_at'),
    }
    return render(request, 'playlist/index.html', data)