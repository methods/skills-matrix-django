from common.tests.custom_classes import LoggedInUserTestCase
from django.urls import reverse


class CareerPathsPageTests(LoggedInUserTestCase):
    def test_GET_logged_in_user(self):
        response = self.client.get(reverse('browse-career-paths'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'career_paths/browse_career_paths.html')
