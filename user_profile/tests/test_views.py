from django.test import TestCase


class LoginPageTests(TestCase):
    def test_login_page_GET(self):
        response = self.client.get('/')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_profile/login.html')

