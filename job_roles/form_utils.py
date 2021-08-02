from super_admin.models import SkillLevel
from app.models import Skill

def get_skill_choices():
    skill_options = [(skill.name, skill.name) for skill in Skill.objects.all()]
    skill_options.insert(0, ('', '--Select a skill--'))
    return skill_options


def get_skill_level_choices():
    skill_level_options = ((skill_level.name, skill_level.name) for skill_level in SkillLevel.objects.all())
    return skill_level_options
