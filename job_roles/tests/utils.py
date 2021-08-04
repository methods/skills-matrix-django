from job_roles.models import Job
from app.models import Skill
from super_admin.models import SkillLevel
from ..forms import JobSkillsAndSkillLevelForm
from django.contrib.auth.models import Group


def creates_job_competency_instances():
    test_job = Job.objects.create(job_title='Test Job')
    test_skill = Skill.objects.create(name='test_skill', skill_type='Career skill')
    test_skill_level = SkillLevel.objects.create(name='test_skill_level')
    return {'test_job': test_job, 'test_skill': test_skill, 'test_skill_level': test_skill_level}


def creates_job_role_skill_and_skill_level_instances():
    Skill.objects.create(name='test_skill_1', skill_type='Career skill')
    Skill.objects.create(name='test_skill_2', skill_type='Career skill')
    Skill.objects.create(name='test_skill_3', skill_type='Career skill')
    Skill.objects.create(name='test_skill_4', skill_type='Career skill')
    SkillLevel.objects.create(name='test_skill_level_2')
    SkillLevel.objects.create(name='test_skill_level_1')
    SkillLevel.objects.create(name='test_skill_level_4')
    SkillLevel.objects.create(name='test_skill_level_3')


def creates_job_role_skill_and_skill_level_form(form_data=None, disabled_choices=None):
    creates_job_role_skill_and_skill_level_instances()
    job_role_skills_form = JobSkillsAndSkillLevelForm(data=form_data, disabled_choices=disabled_choices)
    return job_role_skills_form


def assigns_users_to_a_specific_group(group_name=None, user=None):
    admins_group = Group.objects.get(name=group_name)
    user.groups.add(admins_group)


def saves_job_title_to_session(session=None):
    session['job_role_title'] = 'Test Job Role'
    session.save()


def saves_new_added_job_competencies_to_session(session=None):
    session['new_added_job_competencies'] = [{'test_skill_1': 'test_skill_level_2'},
                                             {'test_skill_2': 'test_skill_level_1'},
                                             {'test_skill_3': 'test_skill_level_4'},
                                             {'test_skill_4': 'test_skill_level_3'}]
    session.save()
