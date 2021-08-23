from app.forms import UserSkillLevelForm
from skills.models import UserCompetencies



def prepare_competency_update(existing_user_skill_id, request):
    if not UserCompetencies.objects.filter(skill=existing_user_skill_id, user=request.user.id).exists():
        form = UserSkillLevelForm()
    else:
        individual_competency = UserCompetencies.objects.get(skill=existing_user_skill_id,user=request.user.id)
        form = UserSkillLevelForm(initial={'user_skill_level': individual_competency.skill_level.name})
    update_existing_skill_id = int(existing_user_skill_id)
    return {'form':form, 'update_existing_skill_id': update_existing_skill_id}

def retrieve_user_skills(user_skills, request):
    all_user_competency = UserCompetencies.objects.filter(user=request.user.id).order_by('id')
    for user_competency in all_user_competency:
        user_skills.append(user_competency.skill.id)
    return user_skills
    