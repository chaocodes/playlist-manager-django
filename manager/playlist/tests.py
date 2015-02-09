from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import Client, TestCase

from manager.song.models import Song

from .models import Playlist

class PlaylistTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('test', password='test')
        user2 = User.objects.create_user('test2', password='test')
        playlist = Playlist.objects.create(name='Rock and Roll', user=user)
        for i in range(0, 10):
            Song.objects.create(name='Rock', artist='n Roll', playlist=playlist)

    # Playlist Functions

    def test_playlist_song_count(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        self.assertEqual(playlist.song_count(), 10)

    def test_playlist_unicode(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        self.assertEqual(playlist.__unicode__(), u'%s - %s' % (playlist.user, playlist.name))

    # Route Helpers

    def authorize(self, auth, wrong_user=False):
        if auth:
            if wrong_user:
                self.client.login(username='test2', password='test')
            else:
                self.client.login(username='test', password='test')
        else:
            self.client.logout()
        return None

    def uri_playlist_all(self, user_id):
        return reverse('playlist:all', args=[user_id])

    def uri_playlist_one(self, user_id, playlist_id):
        return reverse('playlist:one', args=[user_id, playlist_id])

    def uri_playlist_create(self, user_id):
        return reverse('playlist:create', args=[user_id])

    def uri_playlist_edit(self, user_id, playlist_id):
        return reverse('playlist:edit', args=[user_id, playlist_id])

    # Playlist Views

    def test_view_all(self):
        user = User.objects.get(username='test')
        response = self.client.get(self.uri_playlist_all(user.id))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.context['playlists']), 1)
        self.assertTemplateUsed(response, 'playlist/index.html')

    def test_view_one(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.client.get(self.uri_playlist_one(playlist.user.id, playlist.id))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'playlist/playlist.html')

    def test_view_one_noexist(self):
        user = User.objects.get(username='test')
        response = self.client.get(self.uri_playlist_one(user.id, 0))
        self.assertEquals(response.status_code, 404)

    def view_auth(self, uri, auth, wrong_user=False):
        self.authorize(auth, wrong_user)
        response = self.client.get(uri)
        return response

    def test_view_create_auth(self):
        user = User.objects.get(username='test')
        response = self.view_auth(self.uri_playlist_create(user.id), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'playlist/form.html')

    def test_view_create_noauth(self):
        user = User.objects.get(username='test')
        response = self.view_auth(self.uri_playlist_create(user.id), False)
        self.assertEquals(response.status_code, 302)

    def test_view_create_wrongauth(self):
        user = User.objects.get(username='test')
        response = self.view_auth(self.uri_playlist_create(user.id), True, True)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_auth(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_playlist_edit(playlist.user.id, playlist.id), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'playlist/form.html')

    def test_view_edit_noauth(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_playlist_edit(playlist.user.id, playlist.id), False)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_wrongauth(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_playlist_edit(playlist.user.id, playlist.id), True, True)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_noexist(self):
        user = User.objects.get(username='test')
        response = response = self.view_auth(self.uri_playlist_edit(user.id, 0), True)
        self.assertEquals(response.status_code, 404)

    def remove_playlist(self, name):
        playlist = Playlist.objects.filter(name=name)
        if playlist.exists():
            playlist.delete()
        return None

    # Playlist Post Routes

    def form_data_valid(self):
        return {
            'name': 'Playlist',
        }

    def form_data_invalid(self):
        return {}

    def create_playlist(self, data, auth):
        user = User.objects.get(username='test')
        data = data
        self.remove_playlist('Playlist')
        self.authorize(auth)
        response = self.client.post(self.uri_playlist_all(user.id), data)
        return response

    def test_create_playlist_auth(self):
        response = self.create_playlist(self.form_data_valid(), True)
        playlist = Playlist.objects.filter(name='Playlist')
        self.assertEquals(response.status_code, 302)
        self.assertTrue(playlist.exists())

    def test_create_playlist_unauth(self):
        response = self.create_playlist(self.form_data_valid(), False)
        playlist = Playlist.objects.filter(name='Playlist')
        self.assertEquals(response.status_code, 403)
        self.assertFalse(playlist.exists())

    def test_create_playlist_invalid(self):
        response = self.create_playlist(self.form_data_invalid(), True)
        playlist = Playlist.objects.filter(name=None)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFalse(playlist.exists())

    def edit_playlist(self, data, auth):
        user = User.objects.get(username='test')
        self.remove_playlist('Modify This')
        playlist = Playlist.objects.create(name='Modify This', user=user)
        data = data
        self.remove_playlist('Playlist')
        self.authorize(auth)
        response = self.client.post('%s?action=update' % (self.uri_playlist_one(playlist.user.id, playlist.id)), data)
        return response

    def test_edit_playlist_auth(self):
        response = self.edit_playlist(self.form_data_valid(), True)
        playlist = Playlist.objects.filter(name='Playlist')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(playlist.exists())

    def test_edit_playlist_noauth(self):
        response = self.edit_playlist(self.form_data_valid(), False)
        playlist = Playlist.objects.filter(name='Playlist')
        self.assertEquals(response.status_code, 403)
        self.assertFalse(playlist.exists())

    def test_edit_playlist_invalid(self):
        response = self.edit_playlist(self.form_data_invalid(), True)
        playlist = Playlist.objects.filter(name=None)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFalse(playlist.exists())

    def delete_playlist(self, auth):
        user = User.objects.get(username='test')
        self.remove_playlist('Delete This')
        playlist = Playlist.objects.create(name='Delete This', user=user)
        self.authorize(auth)
        response = self.client.post('%s?action=delete' % (self.uri_playlist_one(playlist.user.id, playlist.id)))
        return response

    def test_delete_playlist_auth(self):
        response = self.delete_playlist(True)
        playlist = Playlist.objects.filter(name='Delete This')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(playlist.exists())

    def test_delete_playlist_noauth(self):
        response = self.delete_playlist(False)
        playlist = Playlist.objects.filter(name='Delete This')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(playlist.exists())
