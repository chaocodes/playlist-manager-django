from django.core.urlresolvers import reverse
from django.test import Client, TestCase

class CoreTest(TestCase):
    def setUp(self):
        self.client = Client()

    # Route Helpers

    def uri_home(self):
        return reverse('core:home')

    def uri_playlist(self):
        return reverse('core:playlist')

    def uri_song(self):
        return reverse('core:song')

    # Core Views

    def test_home_view(self):
        response = self.client.get(self.uri_home())
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('core/home.html')

    def test_playlist_view(self):
        response = self.client.get(self.uri_playlist())
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('playlist/index.html')

    def test_song_view(self):
        response = self.client.get(self.uri_song())
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('song/index.html')