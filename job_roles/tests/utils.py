from job_roles.models import Job
from app.models import Skill
from super_admin.models import SkillLevel
from ..forms import JobSkillsAndSkillLevelForm


def creates_job_competency_instances():
    test_job = Job.objects.create(job_title='Test Job')
    test_skill = Skill.objects.create(name='test_skill', skill_type='Career skill')
    test_skill_level = SkillLevel.objects.create(name='test_skill_level')
    return {'test_job': test_job, 'test_skill': test_skill, 'test_skill_level': test_skill_level}


def creates_job_role_skill_and_skill_level_form(form_data=None, disabled_choices=None):
    skill_options = [('skill_1', 'skill_1'), ('skill_2', 'skill_2'),('skill_3', 'skill_3')]
    skill_level_options = [('skill_level_1', 'skill_level_1'), ('skill_level_2', 'skill_level_2'),
                           ('skill_level_3', 'skill_level_3')]
    job_role_skills_form = JobSkillsAndSkillLevelForm(data=form_data, disabled_choices=disabled_choices)
    job_role_skills_form.fields['job_role_skill_level'].choices = skill_level_options
    job_role_skills_form.fields['job_role_skill'].choices = skill_options
    return job_role_skills_form
