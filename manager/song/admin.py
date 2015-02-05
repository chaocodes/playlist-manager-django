from django.contrib import admin

from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'tinysong', 'valid', 'created_at', 'updated_at']

admin.site.register(Song, SongAdmin)