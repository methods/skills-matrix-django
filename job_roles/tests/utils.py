from job_roles.models import Job
from app.models import Skill
from super_admin.models import SkillLevel


def creates_job_competency_instances():
    test_job = Job.objects.create(job_title='Test Job')
    test_skill = Skill.objects.create(name='test_skill', skill_type='Career skill')
    test_skill_level = SkillLevel.objects.create(name='test_skill_level')
    return {'test_job': test_job, 'test_skill': test_skill, 'test_skill_level': test_skill_level}
