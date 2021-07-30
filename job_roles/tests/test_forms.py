from django.test import TestCase
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm
from .utils import creates_job_role_skill_and_skill_level_form


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
        job_role_skills_form = JobSkillsAndSkillLevelForm()
        self.assertFalse(job_role_skills_form.is_bound)

    def test_job_role_skills_form_empty_data_object(self):
        job_role_skills_form = JobSkillsAndSkillLevelForm(data={})
        self.assertTrue(job_role_skills_form.is_bound)
        self.assertFalse(job_role_skills_form.is_valid())

    def test_job_role_skills_form_valid_data(self):
        form_data = {"job_role_skill": 'skill_1', 'job_role_skill_level': 'skill_level_1'}
        job_role_skills_form = creates_job_role_skill_and_skill_level_form(form_data=form_data)
        self.assertTrue(job_role_skills_form.is_valid())

    def test_job_role_skills_form_invalid_data(self):
        form_data = {"job_role_skill": 'skill_5', 'job_role_skill_level': 'skill_level_8'}
        job_role_skills_form = creates_job_role_skill_and_skill_level_form(form_data=form_data)
        self.assertFalse(job_role_skills_form.is_valid())

    def test_job_role_skills_form_disabled_choice_list(self):
        disabled_choices = ['skill_level_1','skill_level_2']
        form_data = {"job_role_skill": 'skill_3', 'job_role_skill_level': 'skill_level_2'}
        job_role_skills_form = creates_job_role_skill_and_skill_level_form(form_data=form_data,
                                                                           disabled_choices=disabled_choices)
        self.assertEqual(job_role_skills_form.fields['job_role_skill'].widget.disabled_choices,
                                                    ['skill_level_1', 'skill_level_2'])

    def test_job_role_skills_form_invalid_disabled_choice_list(self):
        disabled_choices = ['test_skill_level_1','test_skill_level_2']
        form_data = {"job_role_skill": 'skill_3', 'job_role_skill_level': 'skill_level_2'}
        job_role_form = JobSkillsAndSkillLevelForm(data=form_data, disabled_choices=disabled_choices)
        self.assertNotEqual(job_role_form.fields['job_role_skill'].widget.disabled_choices,
                                                ['skill_level_1', 'skill_level_0'])
