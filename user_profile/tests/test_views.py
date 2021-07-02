from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class LoginPageTests(TestCase):
    def test_login_page_GET(self):
        response = self.client.get('')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_profile/login.html')


class LogoutPageTests(TestCase):
    def test_logout_page_GET(self):
        response = self.client.get('/logout')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_profile/logout.html')

    def test_user_logout(self):
        response = self.client.post('/logout', {})
        assert response.status_code == 302
