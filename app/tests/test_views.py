from django.test import TestCase
from django.contrib.auth import get_user_model


class GeneralFunctionalTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user('test@methods.co.uk', 'Test', 'Test', 'OPC',
                                                  'Junior Developer', 'password')
        self.client.login(username='test@methods.co.uk', password='password')

    def test_home_page_status_code(self):
        # breakpoint()
        response = self.client.get('/dashboard')
        assert response.status_code == 200

    def test_home_page_body_resp(self):
        response = self.client.get('/dashboard')
        assert "Welcome" in response.content.decode()

    # def test_edit_skills_button(self):
    #     self.client.get('/dashboard')
    #     button = self.client.find_element_by_class_name('govuk-button')
    #     button.click()
    #     assert '/edit-skills' == self.client.current_url

    def test_user_details(self):
        db = get_user_model()
        db.objects.create_user('ss@user.com', 'userfirstname', 'usersurname', 'userteam', 'userjobrole', 'password')
        response = self.client.get('/dashboard')
        assert "userfirstname" in response.content.decode()
        assert "usersurname" in response.content.decode()
