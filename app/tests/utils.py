from job_roles.models import Job, Competency
from super_admin.models import SkillLevel
from skills.models import Skill


def creates_job_role_title_instance():
    test_job_title = Job.objects.create(job_title='Junior Developer')
    return test_job_title


def creates_skill_instance():
    test_skill = Skill.objects.create(name='test_skill_1')
    return test_skill


def creates_skill_level_instance():
    test_skill_level = SkillLevel.objects.create(name='Beginner')
    return test_skill_level


def creates_job_role_competency_instance():
    Competency.objects.create(job_role_title=creates_job_role_title_instance(),
                              job_role_skill=creates_skill_instance(),
                              job_role_skill_level=creates_skill_level_instance())
