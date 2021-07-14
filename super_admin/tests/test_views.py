from common.tests.custom_classes import LoggedInSuperAdminTestCase


class SkillLevelsPageTests(LoggedInSuperAdminTestCase):
    def test_page_GET_logged_in_super_admin(self):
        response = self.client.get('/super-admin/view-skill-levels')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'super_admin/view_skill_levels.html')
