from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tinysong_key = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u'%s' % (self.user)