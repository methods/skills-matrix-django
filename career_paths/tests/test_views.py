from common.tests.custom_classes import LoggedInUserTestCase


class CareerPathsPageTests(LoggedInUserTestCase):
    def test_GET_logged_in_user(self):
        response = self.client.get('/career-paths/browse')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'career_paths/browse_career_paths.html')
