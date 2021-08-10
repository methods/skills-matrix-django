from common.tests.custom_classes import LoggedInAdminTestCase
from django.urls import reverse
from skills.models import Skill


class ViewSkillsPageTests(LoggedInAdminTestCase):
    def test_GET_request_logged_in_user(self):
        response = self.client.get(reverse('view-skills'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'skills/view_skills.html')

    def test_skill_renders(self):
        Skill.objects.create(name='test_skill')
        response = self.client.get(reverse('view-skills'))
        self.assertContains(response, 'test_skill')

    def test_delete_skill_functionality(self):
        Skill.objects.create(name='test_skill')
        self.client.post(reverse('view-skills'), {'delete': 'test_skill'})
        assert not Skill.objects.filter(name='test_skill').exists()
