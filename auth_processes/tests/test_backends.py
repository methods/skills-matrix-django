from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class LoginPageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        password = make_password('test_password')
        self.user = User.objects.create_user('test@methods.co.uk', 'Test', 'Test', 'OPC', 'Junior Developer', password)
        self.user.save()

    def test_login_page_valid_post(self):
        logged_in = self.client.login(username='test@methods.co.uk', password='test_password')
        assert logged_in is True

    def test_login_page_invalid_post(self):
        logged_in = self.client.login(username='test@test.com', password='test_password2')
        assert logged_in is False
