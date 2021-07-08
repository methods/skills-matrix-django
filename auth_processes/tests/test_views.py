from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class LoginPageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        password = make_password('test_password')
        self.user = User.objects.create_user('test@methods.co.uk', 'Test', 'Test', 'OPC', 'Junior Developer', password)
        self.user.save()

    def test_login_page_GET(self):
        response = self.client.get('/auth/login')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'auth_processes/login.html')

    def test_login_page_valid_credentials(self):
        response = self.client.post('/auth/login', {'username': 'test@methods.co.uk', 'password': 'test_password'})
        assert response.status_code == 302

    def test_login_page_invalid_credentials(self):
        response = self.client.post('/auth/login', {'username': 'test@test.com', 'password': 'test_password2'})
        assert response.status_code != 302


class LogoutPageTests(TestCase):
    def test_logout_page_GET(self):
        response = self.client.get('/auth/logout')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'auth_processes/logout.html')

    def test_user_logout(self):
        response = self.client.post('/auth/logout', {})
        assert response.status_code == 302
