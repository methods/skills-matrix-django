from .models import Competency
from super_admin.models import SkillLevel
from app.models import Skill


def populate_existing_competencies(job):
    competencies = Competency.objects.filter(job_role_title=job.id)
    disabled_choices = []
    for competency in competencies:
        disabled_choices.append(competency.job_role_skill.name)
    return disabled_choices


def get_skill_choices():
    skill_options = ((skill.name, skill.name) for skill in Skill.objects.all())
    return skill_options


def get_skill_level_choices():
    skill_level_options = ((skill_level.name, skill_level.name) for skill_level in SkillLevel.objects.all())
    return skill_level_options

