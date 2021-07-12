from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class DashboardTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        password = make_password('password')
        self.user = self.User.objects.create_user('test@methods.co.uk', 'test_first_name', 'test_surname', 'OPC',
                                                  'Junior Developer', password)
        self.client.login(username='test@methods.co.uk', password='password')

    def tearDown(self):
        self.User.objects.all().delete()

    def test_profile_page_GET_logged_in_user(self):
        response = self.client.get('/profile')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_profile/profile.html')
        assert "test_first_name" in response.content.decode()
        assert "test_surname" in response.content.decode()
        assert "OPC" in response.content.decode()
        assert "Junior Developer" in response.content.decode()

    def test_profile_page_GET_no_user(self):
        self.User.objects.all().delete()
        response = self.client.get('/profile')
        assert response.status_code == 302


