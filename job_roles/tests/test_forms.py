from django.test import TestCase
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm
from .utils import creates_job_role_skill_and_skill_level_form


class TestJobTitleForm(TestCase):

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

    def test_input_capitalised_validation_error_message(self):
        job_role_title_form = JobTitleForm(data={
            'job_role_title': 'junior developer'
        })
        self.assertFalse(job_role_title_form.is_valid())
        self.assertEqual(
            job_role_title_form.errors["job_role_title"], ["The job role title should be capitalised."]
        )

    def test_input_required_validation_error_message(self):
        job_role_title_form = JobTitleForm(data={
            'job_role_title': ''
        })
        self.assertFalse(job_role_title_form.is_valid())
        self.assertEqual(
            job_role_title_form.errors["job_role_title"], ['Enter a job role title']
        )


class TestJobSkillsForm(TestCase):

    def test_job_role_skills_form_no_data(self):
        job_role_skills_form = JobSkillsAndSkillLevelForm()
        self.assertFalse(job_role_skills_form.is_bound)

    def test_job_role_skills_form_empty_data_object(self):
        job_role_skills_form = JobSkillsAndSkillLevelForm(data={})
        self.assertTrue(job_role_skills_form.is_bound)
        self.assertFalse(job_role_skills_form.is_valid())

    def test_job_role_skills_form_valid_data(self):
        form_data = {"job_role_skill": 'test_skill_1', 'job_role_skill_level': 'test_skill_level_1'}
        job_role_skills_form = creates_job_role_skill_and_skill_level_form(form_data=form_data)
        self.assertTrue(job_role_skills_form.is_valid())

    def test_job_role_skills_form_invalid_data(self):
        form_data = {"job_role_skill": 'test_skill_5', 'job_role_skill_level': 'test_skill_level_8'}
        job_role_skills_form = creates_job_role_skill_and_skill_level_form(form_data=form_data)
        self.assertFalse(job_role_skills_form.is_valid())

    def test_job_role_skills_form_disabled_choice_list(self):
        disabled_choices = ['test_skill_level_1', 'test_skill_level_2']
        form_data = {"job_role_skill": 'test_skill_3', 'job_role_skill_level': 'test_skill_level_2'}
        job_role_skills_form = creates_job_role_skill_and_skill_level_form(form_data=form_data,
                                                                           disabled_choices=disabled_choices)
        self.assertTrue(job_role_skills_form.is_valid())
        self.assertEqual(job_role_skills_form.fields['job_role_skill'].widget.disabled_choices,
                                                    ['test_skill_level_1', 'test_skill_level_2'])

    def test_job_role_skills_form_invalid_disabled_choice_list(self):
        disabled_choices = ['test_skill_level_1', 'test_skill_level_2']
        form_data = {"job_role_skill": 'test_skill_3', 'job_role_skill_level': 'test_skill_level_2'}
        job_role_form = creates_job_role_skill_and_skill_level_form(form_data=form_data,
                                                                    disabled_choices=disabled_choices)
        self.assertTrue(job_role_form.is_valid())
        self.assertNotEqual(job_role_form.fields['job_role_skill'].widget.disabled_choices,
                                                ['test_skill_level_1', 'test_skill_level_0'])

    def test_empty_label_selection_raises_error(self):
        form_data = {"job_role_skill": '', 'job_role_skill_level': ''}
        form = creates_job_role_skill_and_skill_level_form(form_data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["job_role_skill"], ["Select a skill"])
        self.assertEqual(form.errors["job_role_skill_level"], ["Select a skill level"])

    def test_select_options_appear_in_form_choices(self):
        form = JobSkillsAndSkillLevelForm()
        assert ('', '--Select a skill--') in form.fields['job_role_skill'].choices
        assert ('', '--Select a skill level--') in form.fields['job_role_skill_level'].choices
