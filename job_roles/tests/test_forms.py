from django.test import TestCase
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm


class TestJobRoleForms(TestCase):
    def test_job_role_title_form_no_data(self):
        job_role_title_form = JobTitleForm()
        self.assertFalse(job_role_title_form.is_bound)

    def test_job_role_title_form_valid_data(self):
        job_role_title_form = JobTitleForm(data={
            'job_role_title': 'Junior Developer'
        })
        self.assertTrue(job_role_title_form.is_valid())

    def test_job_role_title_form_invalid_data(self):
        job_role_title_form = JobTitleForm(data={})
        self.assertTrue(job_role_title_form.is_bound)
        self.assertFalse(job_role_title_form.is_valid())

    def test_input_capitalised_validation(self):
        job_role_title_form = JobTitleForm(data={
            'job_role_title': 'junior developer'
        })
        self.assertEqual(
            job_role_title_form.errors["job_role_title"], ["The job role title should be capitalised."]
        )

    def test_job_role_skills_form_no_data(self):
        job_role_skilss_form = JobSkillsAndSkillLevelForm()
        self.assertFalse(job_role_skilss_form.is_bound)

    def test_job_role_skills_form_invalid_data(self):
        job_role_skilss_form = JobSkillsAndSkillLevelForm(data={})
        self.assertTrue(job_role_skilss_form.is_bound)
        self.assertFalse(job_role_skilss_form.is_valid())
