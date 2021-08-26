from django.test import TestCase
from super_admin.models import Team
from job_roles.models import Job
from django.core.exceptions import ValidationError
from ..validators import validate_domain_email, password_validation
from common.tests.custom_classes import LoggedInUserTestCase
from django.urls import reverse


class AddNameSignup(TestCase):
    def test_signup_add_name_page_status_code(self):
        response = self.client.get(reverse('add-name'))
        assert response.status_code == 200

    def test_signup_add_name_body_resp(self):
        response = self.client.get(reverse('add-name'))
        assert "What is your name?" in response.content.decode()

    def test_valid_submission_redirects_to_email_page(self):
        response = self.client.post(reverse('add-name'), {'first_name': 'user_first_name', 'surname': 'user_surname'})
        self.assertRedirects(response, '/user/signup/email/')


class AddEmailSignup(TestCase):
    def test_signup_add_email_page_status_code(self):
        response = self.client.get(reverse('add-email'))
        assert response.status_code == 200

    def test_signup_add_email_body_resp(self):
        response = self.client.get(reverse('add-email'))
        assert "What is your email address?" in response.content.decode()

    def test_email_session_storage(self):
        self.client.post(reverse('add-email'), {'email': 'test@methods.co.uk'})
        session = self.client.session
        assert session['email_address'] == 'test@methods.co.uk'

    def test_email_domain_validation(self):
        with self.assertRaises(ValidationError):validate_domain_email('test@test.com')
        with self.assertRaises(ValidationError):validate_domain_email('test@test.co.uk')
           


class AddJobSignup(TestCase):
    def test_signup_add_job_page_status_code(self):
        response = self.client.get(reverse('add-job'))
        assert response.status_code == 200

    def test_signup_add_job_body_resp(self):
        response = self.client.get(reverse('add-job'))
        assert "Information about your job" in response.content.decode()

    def test_add_job_submit_redirects_to_password_page(self):
        team=Team()
        team.team_name="OPC"
        team.save()
        job = Job()
        job.job_title = 'Junior Developer'
        job.save()
        response = self.client.post(reverse('add-job'), {'team': 'OPC', 'job_role': 'Junior Developer'})
        self.assertRedirects(response, '/user/signup/create-password/')


class CreatePasswordView(TestCase):
    def test_create_password_status_code(self):
        response = self.client.get(reverse('create-password'))
        assert response.status_code == 200

    def test_create_password_body_resp(self):
        response = self.client.get(reverse('create-password'))
        assert "Create a password" in response.content.decode()

    def test_password_hashing(self):
        self.client.post(reverse('create-password'), {'password': 'password',
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
        response = self.client.get(reverse('summary'))
        assert response.status_code == 200

    def test_check_details_body_resp(self):
        response = self.client.get(reverse('summary'))
        assert "Check your answers" in response.content.decode()


class EditName(TestCase):
    def test_edit_name_page_status_code(self):
        response = self.client.get(reverse('edit-name-signup'))
        assert response.status_code == 200

    def test_edit_name_body_resp(self):
        response = self.client.get(reverse('edit-name-signup'))
        assert "Edit your name" in response.content.decode()

    def test_edit_name_post_request(self):
        self.client.post(reverse('edit-name-signup'), {'first_name': 'Test', 'surname': 'Test Surname'})
        session = self.client.session
        assert session['first_name'] == 'Test'
        assert session['surname'] == 'Test Surname'


class EditEmail(TestCase):
    def test_edit_email_page_status_code(self):
        response = self.client.get(reverse('edit-email-address-signup'))
        assert response.status_code == 200

    def test_edit_email_body_resp(self):
        response = self.client.get(reverse('edit-email-address-signup'))
        assert "Edit your email address" in response.content.decode()

    def test_edit_email_session_storage(self):
        self.client.post(reverse('edit-email-address-signup'), {'email': 'test@methods.co.uk'})
        session = self.client.session
        assert session['email_address'] == 'test@methods.co.uk'


class EditJobInformation(TestCase):
    def test_edit_email_page_status_code(self):
        response = self.client.get(reverse('edit-job-information-signup'))
        assert response.status_code == 200

    def test_edit_email_body_resp(self):
        response = self.client.get(reverse('edit-job-information-signup'))
        assert "Edit your job information" in response.content.decode()

    def test_edit_job_information_post_request(self):
        team = Team()
        team.team_name = "OPC"
        team.save()
        job = Job()
        job.job_title = 'Junior Developer'
        job.save()
        self.client.post(reverse('edit-job-information-signup'), {'team': 'OPC', 'job_role': 'Junior Developer'})
        session = self.client.session
        assert session['job'] == 'Junior Developer'
        assert session['team'] == 'OPC'


class ProfilePageTests(LoggedInUserTestCase):
    def test_profile_page_GET_logged_in_user(self):
        response = self.client.get(reverse('profile'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_management/summary.html')
        assert "test_first_name" in response.content.decode()
        assert "test_surname" in response.content.decode()
        assert "OPC" in response.content.decode()
        assert "Junior Developer" in response.content.decode()

    def test_profile_page_GET_no_user(self):
        self.User.objects.all().delete()
        response = self.client.get(reverse('profile'))
        assert response.status_code == 302


class EditNamePageTests(LoggedInUserTestCase):
    def test_edit_name_page_GET_logged_in_user(self):
        response = self.client.get(reverse('edit-name'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_management/name.html')

    def test_edit_name_page_GET_no_user(self):
        self.User.objects.all().delete()
        response = self.client.get(reverse('edit-name'))
        assert response.status_code == 302

    def test_edit_name_page_POST(self):
        self.client.post(reverse('edit-name'), {'first_name': 'updated_first_name', 'surname': 'updated_surname'})
        self.user.refresh_from_db()
        assert self.user.first_name == 'updated_first_name'
        assert self.user.surname == 'updated_surname'


class EditEmailPageTests(LoggedInUserTestCase):
    def test_edit_email_page_GET_logged_in_user(self):
        response = self.client.get(reverse('edit-email-address'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_management/email_address.html')

    def test_edit_email_page_GET_no_user(self):
        self.User.objects.all().delete()
        response = self.client.get(reverse('edit-email-address'))
        assert response.status_code == 302

    def test_edit_email_POST(self):
        self.client.post(reverse('edit-email-address'), {'email': 'updated@methods.co.uk'})
        self.user.refresh_from_db()
        assert self.user.email == 'updated@methods.co.uk'


class EditJobInformationPageTests(LoggedInUserTestCase):
    def test_edit_email_page_GET_logged_in_user(self):
        response = self.client.get(reverse('edit-job-information'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'user_management/job_info.html')

    def test_edit_job_info_POST(self):
        team = Team()
        team.team_name = "Updated team"
        team.save()
        job = Job()
        job.job_title = 'Updated Job'
        job.save()
        self.client.post(reverse('edit-job-information'), {'team': 'Updated team', 'job_role': 'Updated Job'})
        self.user.refresh_from_db()
        assert self.user.job_role == 'Updated Job'
        assert self.user.team == 'Updated team'

