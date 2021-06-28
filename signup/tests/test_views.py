from django.test import TestCase


class AddNameSignup(TestCase):
    def test_signup_add_name_page_status_code(self):
        response = self.client.get('/signup/name')
        assert response.status_code == 200

    def test_signup_add_name_body_resp(self):
        response = self.client.get('/signup/name')
        assert "What is your name?" in response.content.decode()

    def test_valid_submission_redirects_to_email_page(self):
        response = self.client.post('/signup/name', {'first_name': 'user_first_name', 'surname': 'user_surname'})
        self.assertRedirects(response, '/signup/email/')


class AddJobSignup(TestCase):
    def test_signup_add_job_page_status_code(self):
        response = self.client.get('/signup/job/')
        assert response.status_code == 200

    def test_signup_add_job_body_resp(self):
        response = self.client.get('/signup/job/')
        assert "Information about your job" in response.content.decode()

    def test_add_job_submit_redirects_to_password_page(self):
        response = self.client.post('/signup/job/', {'team': 'OPC', 'job': 'Junior Developer'})
        self.assertRedirects(response, '/signup/create-password/')
