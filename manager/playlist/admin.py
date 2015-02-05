from django.contrib import admin

from manager.song.models import Song

from .models import Playlist

class SongInline(admin.StackedInline):
    model = Song
    extra = 5

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [SongInline]
    list_display = ['name', 'user', 'created_at', 'updated_at']

admin.site.register(Playlist, PlaylistAdmin)