from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import Client

from manager.tests import DBTestCase

from .models import UserProfile

class UserProfileTest(DBTestCase):
    # Route Helpers

    def uri_userprofile_all(self):
        return reverse('userprofile:all')

    def uri_userprofile_one(self, user_id):
        return reverse('userprofile:one', args=[user_id])

    def uri_userprofile_edit(self, user_id):
        return reverse('userprofile:edit', args=[user_id])

    # UserProfile Views

    def test_view_all(self):
        response = self.client.get(self.uri_userprofile_all())
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 2)
        self.assertTemplateUsed(response, 'userprofile/index.html')

    def test_view_one(self):
        user = User.objects.get(username='test')
        response = self.client.get(self.uri_userprofile_one(user.id))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/userprofile.html')

    def test_view_one_noprofile(self):
        user = User.objects.get(username='test2')
        response = self.client.get(self.uri_userprofile_one(user.id))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/userprofile.html')

    def test_view_one_noexist(self):
        response = self.client.get(self.uri_userprofile_one(0))
        self.assertEquals(response.status_code, 404)

    def view_auth(self, uri, auth, wrong_user=False):
        self.authorize(auth, wrong_user)
        response = self.client.get(uri)
        return response

    def test_view_edit_auth(self):
        user = User.objects.get(username='test')
        response = self.view_auth(self.uri_userprofile_edit(user.id), True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/form.html')

    def test_view_edit_noauth(self):
        user = User.objects.get(username='test')
        response = self.view_auth(self.uri_userprofile_edit(user.id), False)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_wrongauth(self):
        user = User.objects.get(username='test')
        response = self.view_auth(self.uri_userprofile_edit(user.id), True, True)
        self.assertEquals(response.status_code, 302)

    def test_view_edit_noprofile(self):
        user = User.objects.get(username='test2')
        response = self.view_auth(self.uri_userprofile_edit(user.id), True, True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/form.html')

    def test_view_edit_noexist(self):
        response = self.view_auth(self.uri_userprofile_edit(0), True)
        self.assertEquals(response.status_code, 404)

    # UserProfile Post Routes

    def form_data_valid(self):
        return {
            'username': 'test',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'tinysong_key': 'key123',
        }

    def form_data_invalid(self):
        return {}

    def edit_userprofile(self, data, auth):
        user = User.objects.get(username='test')
        user.first_name = ''
        user.last_name = ''
        user.save()
        userprofile = UserProfile.objects.get(user=user)
        userprofile.tinysong_key = ''
        userprofile.save()
        self.authorize(auth)
        response = self.client.post('%s?action=update' % (self.uri_userprofile_one(user.id)), data)
        return response

    def test_edit_userprofile_auth(self):
        response = self.edit_userprofile(self.form_data_valid(), True)
        user = User.objects.get(username='test')
        userprofile = UserProfile.objects.filter(tinysong_key='key123', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(userprofile.exists())

    def test_edit_userprofile_noauth(self):
        response = self.edit_userprofile(self.form_data_valid(), False)
        user = User.objects.get(username='test')
        userprofile = UserProfile.objects.filter(tinysong_key='key123', user=user)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(userprofile.exists())

    def test_edit_userprofile_invalid(self):
        response = self.edit_userprofile(self.form_data_invalid(), True)
        user = User.objects.get(username='test')
        userprofile = UserProfile.objects.filter(tinysong_key='key123', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'username', 'This field is required.')
        self.assertFalse(userprofile.exists())