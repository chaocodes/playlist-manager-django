from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PlaylistForm
from .models import Playlist

def form_data(user, form):
    data = {
        'owner': user,
        'playlist_form': form,
    }
    return data

def playlists(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'GET':
        data = {
            'owner': user,
            'playlists': Playlist.objects.filter(user=user),
        }
        return render(request, 'playlist/index.html', data)
    elif request.method == 'POST':
        # Check if user matches URL
        if request.user != user:
            return HttpResponseForbidden()
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('playlist:all', user_id)
        else:
            data = form_data(user, form)
            return render(request, 'playlist/form.html', data)

@login_required
def create_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Check if user matches URL
    if request.user != user:
        return redirect('playlist:create', request.user.id)
    data = form_data(user, PlaylistForm())
    return render(request, 'playlist/form.html', data)

def playlist(request, user_id, playlist_id):
    user = get_object_or_404(User, id=user_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
    if request.method == 'GET':
        data = {
            'owner': user,
            'playlist': playlist,
        }
        return render(request, 'playlist/playlist.html', data)
    elif request.method == 'POST':
        # Check if user owns playlist
        if request.user != playlist.user:
            return HttpResponseForbidden()
        action = request.GET.get('action', False)
        if action:
            if action == 'delete':
                playlist.delete()
            elif action == 'update':
                form = PlaylistForm(request.POST, instance=playlist)
                if form.is_valid():
                    playlist = form.save()
                else:
                    data = form_data(user, form)
                    return render(request, 'playlist/form.html', data)
        return redirect('playlist:all', user_id)

@login_required
def edit_view(request, user_id, playlist_id):
    user = get_object_or_404(User, id=user_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
    # Check if playlist belongs to logged in user
    if request.user != playlist.user:
        return redirect('playlist:all', playlist.user.id)
    data = form_data(user, PlaylistForm(instance=playlist))
    return render(request, 'playlist/form.html', data)