from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from manager.playlist.models import Playlist

from .forms import SongForm
from .models import Song

def form_data(playlist, form):
    data = {
        'playlist': playlist,
        'song_form': form,
    }
    return data

def songs(request, user_id, playlist_id):
    user = get_object_or_404(User, id=user_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
    if request.method == 'GET':
        data = {
            'owner': playlist.user,
            'playlist': playlist,
            'songs': Song.objects.filter(playlist=playlist),
        }
        return render(request, 'song/index.html', data)
    elif request.method == 'POST':
        if request.user != playlist.user:
            return HttpResponseForbidden()
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.playlist = playlist
            song.save()
            return redirect('song:all', user_id, playlist_id)
        else:
            data = form_data(playlist, form)
            return render(request, 'song/form.html', data)

@login_required
def create_view(request, user_id, playlist_id):
    user = get_object_or_404(User, id=user_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
    # Check if user owns playlist
    if request.user != playlist.user:
        return redirect('song:all', user_id, playlist_id)
    data = form_data(playlist, SongForm())
    return render(request, 'song/form.html', data)

def song(request, user_id, playlist_id, song_id):
    user = get_object_or_404(User, id=user_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
    song = get_object_or_404(Song, id=song_id, playlist=playlist)
    if request.method == 'GET':
        data = {
            'owner': playlist.user,
            'playlist': playlist,
            'song': song,
        }
        return render(request, 'song/song.html', data)
    elif request.method == 'POST':
        # Check if user owns playlist
        if request.user != playlist.user:
            return HttpResponseForbidden()
        action = request.GET.get('action', False)
        if action:
            if action == 'delete':
                song.delete()
                return redirect('song:all', user_id, playlist_id)
            elif action == 'update':
                form = SongForm(request.POST, instance=song)
                if form.is_valid():
                    song = form.save()
                else:
                    data = form_data(playlist, form)
                    return render(request, 'song/form.html', data)
        return redirect('song:all', user_id, playlist_id)

@login_required
def edit_view(request, user_id, playlist_id, song_id):
    user = get_object_or_404(User, id=user_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
    # Check if user owns playlist
    if request.user != playlist.user:
        return redirect('song:all', user_id, playlist_id)
    song = get_object_or_404(Song, id=song_id, playlist=playlist)
    data = form_data(playlist, SongForm(instance=song))
    return render(request, 'song/form.html', data)