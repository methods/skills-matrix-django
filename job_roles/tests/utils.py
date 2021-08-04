from job_roles.models import Job
from app.models import Skill
from super_admin.models import SkillLevel
from ..forms import JobSkillsAndSkillLevelForm


def creates_job_competency_instances():
    test_job = Job.objects.create(job_title='Test Job')
    test_skill = Skill.objects.create(name='test_skill', skill_type='Career skill')
    test_skill_level = SkillLevel.objects.create(name='test_skill_level')
    return {'test_job': test_job, 'test_skill': test_skill, 'test_skill_level': test_skill_level}


def creates_job_role_skill_and_skill_level_instances():
    Skill.objects.create(name='skill_1', skill_type='Career skill')
    Skill.objects.create(name='skill_2', skill_type='Career skill')
    Skill.objects.create(name='skill_3', skill_type='Career skill')
    Skill.objects.create(name='skill_4', skill_type='Career skill')
    SkillLevel.objects.create(name='skill_level_2')
    SkillLevel.objects.create(name='skill_level_1')
    SkillLevel.objects.create(name='skill_level_4')
    SkillLevel.objects.create(name='skill_level_3')


def creates_job_role_skill_and_skill_level_form(form_data=None, disabled_choices=None):
    creates_job_role_skill_and_skill_level_instances()
    job_role_skills_form = JobSkillsAndSkillLevelForm(data=form_data, disabled_choices=disabled_choices)
    return job_role_skills_form
