from common.tests.custom_classes import LoggedInUserTestCase
from django.urls import reverse


class DashboardTests(LoggedInUserTestCase):

    def test_home_page_status_code(self):
        response = self.client.get(reverse('dashboard'))
        assert response.status_code == 200

    def test_home_page_body_resp(self):
        response = self.client.get(reverse('dashboard'))
        assert "Welcome" in response.content.decode()

    def test_user_details(self):
        response = self.client.get(reverse('dashboard'))
        assert "test_first_name" in response.content.decode()
        assert "OPC" in response.content.decode()
        assert "Junior Developer" in response.content.decode()
        self.assertNotIn('test_surname', response.content.decode())


class BrowseProfileTests(LoggedInUserTestCase):

    def test_status_code(self):
        response = self.client.get(reverse('browse-profiles'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'app/browse_profiles.html')
