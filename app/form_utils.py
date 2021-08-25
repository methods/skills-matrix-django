from skills.models import Skill


def get_all_available_skills():
    skill_options = [(skill.name, skill.name) for skill in Skill.objects.all()]
    skill_options.insert(0, ('', '--Select a skill--'))
    return skill_options