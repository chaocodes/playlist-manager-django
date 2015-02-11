from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from manager.tests import DBTestCase

from manager.playlist.models import Playlist

from .models import Song

class SongTest(DBTestCase):
    # Route Helpers

    def uri_song_all(self, user_id, playlist_id):
        return reverse('song:all', args=[user_id, playlist_id])

    def uri_song_one(self, user_id, playlist_id, song_id):
        return reverse('song:one', args=[user_id, playlist_id, song_id])

    def uri_song_create(self, user_id, playlist_id):
        return reverse('song:create', args=[user_id, playlist_id])

    def uri_song_edit(self, user_id, playlist_id, song_id):
        return reverse('song:edit', args=[user_id, playlist_id, song_id])

    # Song Views

    def test_view_all(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.client.get(self.uri_song_all(playlist.user.id, playlist.id))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.context['songs']), 10)
        self.assertTemplateUsed(response, 'song/index.html')

    def test_view_one(self):
        song = Song.objects.all()[0]
        response = self.client.get(self.uri_song_one(song.playlist.user.id, song.playlist.id, song.id))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'song/song.html')

    def test_view_one_noexist(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.client.get(self.uri_song_one(playlist.user.id, playlist.id, 0))
        self.assertEquals(response.status_code, 404)

    def view_auth(self, uri, auth, wrong_user=False):
        self.authorize(auth, wrong_user)
        response = self.client.get(uri)
        return response

    def test_view_create_auth(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_song_create(playlist.user.id, playlist.id), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'song/form.html')

    def test_view_create_noauth(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_song_create(playlist.user.id, playlist.id), False)
        self.assertEquals(response.status_code, 302)

    def test_view_create_wrongauth(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_song_create(playlist.user.id, playlist.id), True, True)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_auth(self):
        song = Song.objects.all()[0]
        response = self.view_auth(self.uri_song_edit(song.playlist.user.id, song.playlist.id, song.id), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'song/form.html')

    def test_view_edit_noauth(self):
        song = Song.objects.all()[0]
        response = self.view_auth(self.uri_song_edit(song.playlist.user.id, song.playlist.id, song.id), False)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_wrongauth(self):
        song = Song.objects.all()[0]
        response = self.view_auth(self.uri_song_edit(song.playlist.user.id, song.playlist.id, song.id), True, True)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_noexist(self):
        playlist = Playlist.objects.get(name='Rock and Roll')
        response = self.view_auth(self.uri_song_edit(playlist.user.id, playlist.id, 0), True)
        self.assertEquals(response.status_code, 404)

    def remove_song(self, name):
        song = Song.objects.filter(name=name).delete()
        return None

    # Song Post Routes

    def form_data_valid(self):
        return {
            'name': 'Stairway to Heaven',
            'artist': 'Led Zeppelin',
            'tinysong': 'http://tinysong.com/xy1v',
        }

    def form_data_invalid(self):
        return {
            'artist': 'No Song Name',
        }

    def create_song(self, data, auth):
        playlist = Playlist.objects.get(name='Rock and Roll')
        self.remove_song('Stairway to Heaven')
        self.authorize(auth)
        response = self.client.post(self.uri_song_all(playlist.user.id, playlist.id), data)
        return response

    def test_create_song_auth(self):
        response = self.create_song(self.form_data_valid(), True)
        song = Song.objects.filter(name='Stairway to Heaven')
        self.assertEquals(response.status_code, 302)
        self.assertTrue(song.exists())

    def test_create_song_noauth(self):
        response = self.create_song(self.form_data_valid(), False)
        song = Song.objects.filter(name='Stairway to Heaven')
        self.assertEquals(response.status_code, 403)
        self.assertFalse(song.exists())

    def test_create_song_invalid(self):
        response = self.create_song(self.form_data_invalid(), True)
        song = Song.objects.filter(artist='No Song Name')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFalse(song.exists())

    def edit_song(self, data, auth):
        playlist = Playlist.objects.get(name='Rock and Roll')
        self.remove_song('Modify This')
        song = Song.objects.create(name='Modify This', artist='Modify This', playlist=playlist)
        self.remove_song('Stairway To Heaven')
        self.authorize(auth)
        response = self.client.post('%s?action=update' % (self.uri_song_one(song.playlist.user.id, song.playlist.id, song.id)), data)
        return response

    def test_edit_song_auth(self):
        response = self.edit_song(self.form_data_valid(), True)
        song = Song.objects.filter(name='Stairway to Heaven')
        self.assertEquals(response.status_code, 302)
        self.assertTrue(song.exists())

    def test_edit_song_noauth(self):
        response = self.edit_song(self.form_data_valid(), False)
        song = Song.objects.filter(name='Stairway to Heaven')
        self.assertEquals(response.status_code, 403)
        self.assertFalse(song.exists())

    def test_edit_song_invalid(self):
        response = self.edit_song(self.form_data_invalid(), True)
        song = Song.objects.filter(artist='No Song Name')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFalse(song.exists())

    def delete_song(self, auth):
        playlist = Playlist.objects.get(name='Rock and Roll')
        self.remove_song('Delete This')
        song = Song.objects.create(name='Delete This', artist='Delete This', playlist=playlist)
        self.authorize(auth)
        response = self.client.post('%s?action=delete' % (self.uri_song_one(song.playlist.user.id, song.playlist.id, song.id)))
        return response

    def test_delete_song_auth(self):
        response = self.delete_song(True)
        song = Song.objects.filter(name='Delete This')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(song.exists())

    def test_delete_song_noauth(self):
        response = self.delete_song(False)
        song = Song.objects.filter(name='Delete This')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(song.exists())