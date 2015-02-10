from django.contrib.auth.models import User
from django.test import Client, TestCase

from manager.playlist.models import Playlist
from manager.song.models import Song

class DBTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('test', password='test')
        user2 = User.objects.create_user('test2', password='test')
        playlist = Playlist.objects.create(name='Rock and Roll', user=user)
        for i in range(0, 10):
            Song.objects.create(name='Rock', artist='n Roll', playlist=playlist)

    def tearDown(self):
        Song.objects.all().delete()
        Playlist.objects.all().delete()
        User.objects.all().delete()

    def authorize(self, auth, wrong_user=False):
        if auth:
            if wrong_user:
                self.client.login(username='test2', password='test')
            else:
                self.client.login(username='test', password='test')
        else:
            self.client.logout()
        return None