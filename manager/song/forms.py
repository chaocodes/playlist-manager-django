from django.forms import ModelForm

from .models import Song

class SongForm(ModelForm):
    class Meta:
        model = Song
        exclude = ['playlist', 'created_at', 'updated_at', 'valid']