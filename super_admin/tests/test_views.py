from common.tests.custom_classes import LoggedInSuperAdminTestCase
from ..models import SkillLevel


class SkillLevelsPageTests(LoggedInSuperAdminTestCase):
    def test_page_GET_logged_in_super_admin(self):
        response = self.client.get('/super-admin/view-skill-levels')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'super_admin/view_skill_levels.html')

    def test_delete_skill_level(self):
        SkillLevel.objects.create(name='test')
        self.client.post('/super-admin/view-skill-levels', {'delete': ['test']})
        assert SkillLevel.objects.count() == 0


class AddSkillLevelPageTests(LoggedInSuperAdminTestCase):
    def test_page_GET_logged_in_super_admin(self):
        response = self.client.get('/super-admin/add-a-skill-level/')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'super_admin/add_skill_level.html')

    def test_post_request(self):
        self.client.post('/super-admin/add-a-skill-level/', {'name': 'test', 'description': 'test'})
        assert SkillLevel.objects.filter(name='test').exists()

