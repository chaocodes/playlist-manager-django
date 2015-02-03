from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserForm, UserProfileForm

from .models import UserProfile

def form_data(user_form, userprofile_form):
    data = {
        'user_form': user_form,
        'userprofile_form': userprofile_form,
    }
    return data

def users(request):
    users = User.objects.all()
    data = {
        'users': users,
    }
    return render(request, 'userprofile/index.html', data)

def user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None
    if request.method == 'GET':
        data = {
            'owner': user,
            'userprofile': userprofile,
        }
        return render(request, 'userprofile/userprofile.html', data)
    elif request.method == 'POST':
        # Check that you are the user you want to edit
        if request.user != user:
            return HttpResponseForbidden()
        action = request.GET.get('action', False)
        if action:
            if action == 'update':
                user_form = UserForm(request.POST, instance=user)
                userprofile_form = UserProfileForm(request.POST, instance=userprofile)
                if user_form.is_valid() and userprofile_form.is_valid():
                    user = user_form.save()
                    userprofile = userprofile_form.save(commit=False)
                    userprofile.user = user
                    userprofile.save()
                else:
                    data = form_data(user_form, userprofile_form)
                    return render(request, 'userprofile/form.html', data)
        return redirect('userprofile:one', user_id)

@login_required
def edit_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Check that you are the user you want to edit
    if request.user != user:
        return redirect('userprofile:edit', request.user.id)
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None
    data = form_data(UserForm(instance=user), UserProfileForm(instance=userprofile))
    return render(request, 'userprofile/form.html', data)