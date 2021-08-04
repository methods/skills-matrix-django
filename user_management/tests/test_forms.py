from django.test import SimpleTestCase, TestCase
from ..forms import NameForm, EmailForm, PasswordForm, JobForm


class TestForms(SimpleTestCase):
    def test_name_form_valid_data(self):
        form = NameForm(data={
            'first_name': 'user',
            'surname': 'user_surname'
        })

        assert form.is_valid()

    def test_name_form_invalid_data(self):
        form = NameForm(data={})

        assert not form.is_valid()

    def test_email_form_valid_data(self):
        form = EmailForm(data={
            'email_address': "test@methods.co.uk"
        })
        assert form.is_valid()

    def test_email_form_invalid_data(self):
        form = EmailForm(data={
            'email_address': "test"
        })
        assert not form.is_valid()

    def test_create_password_form(self):
        form = PasswordForm(data={
            'password': 'password',
            'password_confirm': 'password'
        })
        assert form.is_valid()

    def test_create_password_form_invalid_data(self):
        form = PasswordForm(data={
            'password': 'password',
            'password_confirm': 'password2'
        })
        assert not form.is_valid()


class JobFormTests(TestCase):
    def test_add_job_form(self):
        form = JobForm()
        assert ('', '--Select a team--') in form.fields['team'].choices
        assert ('', '--Select a job--') in form.fields['job'].choices

    def test_form_submit_empty_strings(self):
        form = JobForm({'team': '', 'job': ''})
        assert not form.is_valid()
        self.assertEqual(form.errors['team'], ['Select a team'])
        self.assertEqual(form.errors['job'], ['Select a job'])

