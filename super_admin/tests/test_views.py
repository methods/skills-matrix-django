from common.tests.custom_classes import LoggedInSuperAdminTestCase
from ..models import SkillLevel


class SkillLevelsPageTests(LoggedInSuperAdminTestCase):
    def test_page_GET_logged_in_super_admin(self):
        response = self.client.get('/super-admin/view-skill-levels/')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'super_admin/view_skill_levels.html')

    def test_delete_skill_level(self):
        SkillLevel.objects.create(name='test')
        self.client.post('/super-admin/view-skill-levels/', {'delete': ['test']})
        assert SkillLevel.objects.count() == 0


class AddSkillLevelPageTests(LoggedInSuperAdminTestCase):
    def test_page_GET_logged_in_super_admin(self):
        response = self.client.get('/super-admin/add-a-skill-level/')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'super_admin/skill_level.html')

    def test_post_request(self):
        self.client.post('/super-admin/add-a-skill-level/', {'name': 'test', 'description': 'test'})
        assert SkillLevel.objects.filter(name='test').exists()


class EditSkillLevelPageTests(LoggedInSuperAdminTestCase):
    def setUp(self):
        super(EditSkillLevelPageTests, self).setUp()
        self.test_skill_level = SkillLevel.objects.create(name='test')
        self.pk = self.test_skill_level.pk


    def test_page_GET_logged_in_super_admin(self):
        response = self.client.get(f"/super-admin/edit-skill-level/{self.pk}/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'super_admin/skill_level.html')

    def test_post_request(self):
        self.client.post(f"/super-admin/edit-skill-level/{self.pk}/", {'name': 'update_test',
                                                                       'description': 'update_description'})
        self.test_skill_level.refresh_from_db()
        assert self.test_skill_level.name == 'update_test'
        assert self.test_skill_level.description == 'update_description'
