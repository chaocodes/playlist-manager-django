from django.forms import ModelForm

from .models import Playlist

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        exclude = ['user', 'created_at', 'updated_at']