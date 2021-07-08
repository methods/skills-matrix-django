from django.test import TestCase
from super_admin.models import Team
from job_roles.models import Job
from django.core.exceptions import ValidationError
from ..validators import validate_domain_email,password_validation


class AddNameSignup(TestCase):
    def test_signup_add_name_page_status_code(self):
        response = self.client.get('/signup/name')
        assert response.status_code == 200

    def test_signup_add_name_body_resp(self):
        response = self.client.get('/signup/name')
        assert "What is your name?" in response.content.decode()

    def test_valid_submission_redirects_to_email_page(self):
        response = self.client.post('/signup/name', {'first_name': 'user_first_name', 'surname': 'user_surname'})
        self.assertRedirects(response, '/signup/email')


class AddEmailSignup(TestCase):
    def test_signup_add_email_page_status_code(self):
        response = self.client.get('/signup/email')
        assert response.status_code == 200

    def test_signup_add_email_body_resp(self):
        response = self.client.get('/signup/email')
        assert "What is your email address?" in response.content.decode()

    def test_email_session_storage(self):
        self.client.post('/signup/email', {'email_address': 'test@methods.co.uk'})
        session = self.client.session
        assert session['email_address'] == 'test@methods.co.uk'

    def test_email_domain_validation(self):
        with self.assertRaises(ValidationError):validate_domain_email('test@test.com')
        with self.assertRaises(ValidationError):validate_domain_email('test@test.co.uk')
           


class AddJobSignup(TestCase):
    def test_signup_add_job_page_status_code(self):
        response = self.client.get('/signup/job')
        assert response.status_code == 200

    def test_signup_add_job_body_resp(self):
        response = self.client.get('/signup/job')
        assert "Information about your job" in response.content.decode()

    def test_add_job_submit_redirects_to_password_page(self):
        team=Team()
        team.team_name="OPC"
        team.save()
        job = Job()
        job.job_title = 'Junior Developer'
        job.save()
        response = self.client.post('/signup/job', {'team': 'OPC', 'job': 'Junior Developer'})
        self.assertRedirects(response, '/signup/create-password')


class CreatePasswordView(TestCase):
    def test_create_password_status_code(self):
        response = self.client.get('/signup/create-password')
        assert response.status_code == 200

    def test_create_password_body_resp(self):
        response = self.client.get('/signup/create-password')
        assert "Create a password" in response.content.decode()

    def test_password_hashing(self):
        self.client.post('/signup/create-password', {'password': 'password',
                                                                 'password_confirm': 'password'})
        session = self.client.session
        assert not session['hashed_password'] == 'password'
    
    def test_password_validation(self):
        with self.assertRaisesRegex(ValidationError, 'Password length must be greater than 8 character.'):
            password_validation('test')
        with self.assertRaisesRegex(ValidationError, 'Password must contain at least 1 digit.'):
            password_validation('testtest')
        with self.assertRaisesRegex(ValidationError, 'Password must contain at least 6 letter.'):
            password_validation('11221123311')
        with self.assertRaisesRegex(ValidationError, 'Password must contain at least 1 special character.'):
            password_validation('aaasbj22')
        
class CheckDetailsSummary(TestCase):
    def test_check_details_page_status_code(self):
        response = self.client.get('/signup/summary')
        assert response.status_code == 200

    def test_check_details_body_resp(self):
        response = self.client.get('/signup/summary')
        assert "Check your answers" in response.content.decode()


class EditName(TestCase):
    def test_edit_name_page_status_code(self):
        response = self.client.get('/signup/edit-name')
        assert response.status_code == 200

    def test_edit_name_body_resp(self):
        response = self.client.get('/signup/edit-name')
        assert "Edit your name" in response.content.decode()

    def test_edit_name_post_request(self):
        self.client.post('/signup/edit-name', {'first_name': 'Test', 'surname': 'Test Surname'})
        session = self.client.session
        assert session['first_name'] == 'Test'
        assert session['surname'] == 'Test Surname'


class EditEmail(TestCase):
    def test_edit_email_page_status_code(self):
        response = self.client.get('/signup/edit-email-address')
        assert response.status_code == 200

    def test_edit_email_body_resp(self):
        response = self.client.get('/signup/edit-email-address')
        assert "Edit your email address" in response.content.decode()

    def test_edit_email_session_storage(self):
        self.client.post('/signup/edit-email-address', {'email_address': 'test@methods.co.uk'})
        session = self.client.session
        assert session['email_address'] == 'test@methods.co.uk'


class EditJobInformation(TestCase):
    def test_edit_email_page_status_code(self):
        response = self.client.get('/signup/edit-job-information')
        assert response.status_code == 200

    def test_edit_email_body_resp(self):
        response = self.client.get('/signup/edit-job-information')
        assert "Edit your job information" in response.content.decode()

    def test_edit_job_information_post_request(self):
        team = Team()
        team.team_name = "OPC"
        team.save()
        job = Job()
        job.job_title = 'Junior Developer'
        job.save()
        self.client.post('/signup/edit-job-information', {'team': 'OPC', 'job': 'Junior Developer'})
        session = self.client.session
        assert session['job'] == 'Junior Developer'
        assert session['team'] == 'OPC'
