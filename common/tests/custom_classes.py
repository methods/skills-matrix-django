from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


class LoggedInUserTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        password = make_password('password')
        self.user = self.User.objects.create_user('test@methods.co.uk', 'test_first_name', 'test_surname', 'OPC',
                                                  'Junior Developer', password)
        self.client.login(username='test@methods.co.uk', password='password')

    def tearDown(self):
        self.User.objects.all().delete()
