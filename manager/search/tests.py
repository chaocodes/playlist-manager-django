from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import Client

from manager.tests import DBTestCase

from manager.userprofile.models import UserProfile

class SearchTest(DBTestCase):
    # Route Helpers

    def uri_search_songs(self):
        return reverse('search:songs')

    # Search Views

    def view_auth(self, uri, auth, wrong_user=False):
        self.authorize(auth, wrong_user)
        response = self.client.get(uri)
        return response

    def set_key(self, key):
        user = User.objects.get(username='test')
        userprofile = UserProfile.objects.get(user=user)
        userprofile.tinysong_key = key
        userprofile.save()

    def test_view_search_songs_key(self):
        self.set_key('key123')
        response = self.view_auth(self.uri_search_songs(), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/index.html')

    def test_view_search_songs_nokey(self):
        self.set_key('')
        response = self.view_auth(self.uri_search_songs(), True)
        self.assertEquals(response.status_code, 302)

    def test_view_search_songs_noprofile(self):
        response = self.view_auth(self.uri_search_songs(), True, True)
        self.assertEquals(response.status_code, 302)

    # Search Post Routes

    def form_data_valid(self):
        return {
            'criteria': 'The Beatles',
        }

    def form_data_invalid(self):
        return {}