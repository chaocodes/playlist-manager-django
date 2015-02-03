from django.db import models

from manager.playlist.models import Playlist

class Song(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    tinysong = models.URLField(max_length=200, blank=True)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    playlist = models.ForeignKey(Playlist)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.playlist, self.name, self.artist)