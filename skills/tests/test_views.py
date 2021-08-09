from common.tests.custom_classes import LoggedInAdminTestCase
from django.urls import reverse


class ViewSkillsPageTests(LoggedInAdminTestCase):
    def test_GET_request_logged_in_user(self):
        response = self.client.get(reverse('view-skills'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'skills/view_skills.html')
