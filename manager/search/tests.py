from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from mock import Mock, patch

from manager.tests import DBTestCase

from manager.userprofile.models import UserProfile

from .views import tinysong_search

class SearchTest(DBTestCase):
    # Search Functions

    def test_tinysong_search(self):
        with patch('manager.search.views.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'Url': 'http://tinysong.com/15NfR',
                'SongID': 36169931,
                'SongName': 'Hey Jude',
                'ArtistID': 1692349,
                'ArtistName': 'The Silver Beetles',
                'AlbumID': 8005025,
                'AlbumName': 'Beatles Covers Collection',
            }
            results = tinysong_search('The Beatles', 1, 'key123')
            self.assertEquals(results, mock_response.json.return_value)

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

    def post_auth(self, uri, data, auth):
        self.authorize(auth)
        response = self.client.post(uri, data)
        return response

    def test_search_noformat(self):
        self.set_key('key123')
        response = self.post_auth(self.uri_search_songs(), self.form_data_valid(), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/results.html')

    def test_search_noformat_invalid(self):
        self.set_key('key123')
        response = self.post_auth(self.uri_search_songs(), self.form_data_invalid(), True)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'criteria', 'This field is required.')

    def test_search_ajaxformat(self):
        self.set_key('key123')
        response = self.post_auth('%s?format=ajax' % (self.uri_search_songs()), self.form_data_valid(), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/ajax.html')