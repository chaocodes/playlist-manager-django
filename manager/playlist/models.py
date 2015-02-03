from django.contrib.auth.models import User
from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def song_count(self):
        return self.song_set.count()

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.name)