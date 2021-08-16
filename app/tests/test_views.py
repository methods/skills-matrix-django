from common.tests.custom_classes import LoggedInUserTestCase
from django.urls import reverse
from .utils import creates_job_role_title_instance, creates_job_role_competency_instance


class DashboardTests(LoggedInUserTestCase):

    def test_home_page_status_code(self):
        creates_job_role_title_instance()
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'app/dashboard.html')
        assert response.status_code == 200

    def test_home_page_body_resp(self):
        creates_job_role_title_instance()
        response = self.client.get(reverse('dashboard'))
        assert "Welcome" in response.content.decode()

    def test_user_details(self):
        creates_job_role_title_instance()
        response = self.client.get(reverse('dashboard'))
        assert "test_first_name" in response.content.decode()
        assert "OPC" in response.content.decode()
        assert "Junior Developer" in response.content.decode()
        self.assertNotIn('test_surname', response.content.decode())

    def test_message_renders_when_no_skills(self):
        creates_job_role_title_instance()
        response = self.client.get(reverse('dashboard'))
        self.assertIn('Sorry, but at the moment this job role has no skills assigned to.',
                      response.content.decode())

    def test_skill_skill_levels_renders(self):
        creates_job_role_competency_instance()
        response = self.client.get(reverse('dashboard'))
        assert "test_skill_1" in response.content.decode()
        assert "test_skill_level_1" in response.content.decode()
        self.assertNotIn('Sorry, but at the moment this job role has no skills assigned to.',
                         response.content.decode())


class BrowseProfileTests(LoggedInUserTestCase):

    def test_status_code(self):
        response = self.client.get(reverse('browse-profiles'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'app/browse_profiles.html')
