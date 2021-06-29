from django.test import TestCase
from django.apps import apps




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
        Team = apps.get_model('super_admin', 'Team')
        team = Team()
        team.team_name = "OPC"
        team.save()
        Job = apps.get_model('admin_user', 'Job')
        job = Job()
        job.job_title = 'Junior Developer'
        job.save()
        print(Team.objects.all())
        response = self.client.post('/signup/job/', {'team': 'OPC', 'job': 'Junior Developer'})
        self.assertRedirects(response, '/signup/create-password/')


# class CheckDetailsSummary(TestCase):
#     def test_check_details_page_status_code(self):
#         response = self.client.get('/signup/summary/')
#         assert response.status_code == 200
#
#     def test_check_details_body_resp(self):
#         response = self.client.get('/signup/summary/')
#         assert "Check your answers" in response.content.decode()


class EditName(TestCase):
    def test_edit_name_page_status_code(self):
        response = self.client.get('/signup/edit-name/')
        assert response.status_code == 200

    def test_edit_name_body_resp(self):
        response = self.client.get('/signup/edit-name/')
        assert "Edit your name" in response.content.decode()


class EditEmail(TestCase):
    def test_edit_email_page_status_code(self):
        response = self.client.get('/signup/edit-email-address/')
        assert response.status_code == 200

    def test_edit_email_body_resp(self):
        response = self.client.get('/signup/edit-email-address/')
        assert "Edit your name" in response.content.decode()


class EditJobInformation(TestCase):
    def test_edit_email_page_status_code(self):
        response = self.client.get('/signup/edit-job-information/')
        assert response.status_code == 200

    def test_edit_email_body_resp(self):
        response = self.client.get('/signup/edit-job-information/')
        assert "Edit your name" in response.content.decode()