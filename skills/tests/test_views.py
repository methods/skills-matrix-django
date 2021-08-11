from common.tests.custom_classes import LoggedInAdminTestCase
from django.urls import reverse
from skills.models import Skill
from super_admin.models import Team


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
        test_skill = Skill.objects.create(name='test_skill')
        self.client.post(reverse('view-skills'), {'delete': test_skill.id})
        assert not Skill.objects.filter(name='test_skill').exists()


class AddSkillPageTests(LoggedInAdminTestCase):
    def test_GET_request_logged_in_user(self):
        response = self.client.get(reverse('admin-create-skill'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'skills/create_skill.html')

    def test_valid_POST_request(self):
        test_team = Team.objects.create(team_name='test_team')
        self.client.post(reverse('admin-create-skill'), {'skill_name': 'Test skill', 'team': 'test_team'})
        assert Skill.objects.filter(name='Test skill', team=test_team).exists()