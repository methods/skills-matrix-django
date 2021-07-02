from django.test import SimpleTestCase
from ..forms import NameForm, EmailForm, PasswordForm


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
