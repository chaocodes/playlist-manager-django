from django.contrib import admin

from manager.song.models import Song

from .models import Playlist

class SongInline(admin.StackedInline):
    model = Song
    extra = 5

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [SongInline]

admin.site.register(Playlist, PlaylistAdmin)