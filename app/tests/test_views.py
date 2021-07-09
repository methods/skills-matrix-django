from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class GeneralFunctionalTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        password = make_password('password')
        self.user = self.User.objects.create_user('test@methods.co.uk', 'test_first_name', 'test_surname', 'OPC',
                                                  'Junior Developer', password)
        self.client.login(username='test@methods.co.uk', password='password')

    def tearDown(self):
        self.User = get_user_model()
        self.User.objects.all().delete()

    def test_home_page_status_code(self):
        response = self.client.get('/dashboard')
        assert response.status_code == 200

    def test_home_page_body_resp(self):
        response = self.client.get('/dashboard')
        assert "Welcome" in response.content.decode()

    def test_user_details(self):
        response = self.client.get('/dashboard')
        assert "test_first_name" in response.content.decode()
        assert "test_surname" in response.content.decode()
