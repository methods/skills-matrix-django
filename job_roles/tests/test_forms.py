from django.test import SimpleTestCase
from job_roles.forms import JobTitleForm


class TestJobRoleForms(SimpleTestCase):
    def test_job_role_form_valid_data(self):
        form = JobTitleForm(data={
            'job_role_title': 'Junior Developer'
        })
        assert form.is_valid()

    def test_job_role_form_no_data(self):
        form = JobTitleForm(data={})
        assert not form.is_valid()

    def test_input_capitalised_validation(self):
        form = JobTitleForm(data={
            'job_role_title': 'junior developer'
        })
        self.assertEqual(
            form.errors["job_role_title"], ["The job role title should be capitalised."]
        )
