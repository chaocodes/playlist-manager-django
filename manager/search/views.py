from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from manager.playlist.models import Playlist
from manager.userprofile.models import UserProfile

from .forms import SearchForm

import requests

def tinysong_search(criteria, limit, key):
    params = {
        'format': 'json',
        'limit': limit,
        'key': key,
    }
    results = requests.get('http://tinysong.com/s/' + criteria, params=params)
    return results.json()

@login_required
def search(request):
    # Check if userprofile exists and there is a valid tinysong key
    user = request.user
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return redirect('userprofile:edit', request.user.id)
    if userprofile.tinysong_key == '':
        return redirect('userprofile:edit', request.user.id)

    if request.method == 'GET':
        data = {
            'search_form': SearchForm()
        }
        return render(request, 'search/index.html', data)
    elif request.method == 'POST':
        tinysong_key = userprofile.tinysong_key
        form = SearchForm(request.POST)
        if form.is_valid():
            data = {
                'results': tinysong_search(form.cleaned_data['criteria'], 30, tinysong_key),
                'playlists': Playlist.objects.filter(user=request.user),
            }
        else:
            data = {
                'search_form': form,
            }
            return render(request, 'search/index.html', data)
        format = request.GET.get('format', False)
        if format:
            if format == 'json':
                return JsonResponse(data)
            elif format == 'ajax':
                return render(request, 'search/ajax.html', data)
        return render(request, 'search/results.html', data)