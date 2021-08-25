from app.forms import UserSkillLevelForm, UserSkillDefinitionForm
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


def prepare_non_job_related_competency_update(existing_user_competency_id, request):
    user_competency_object = UserCompetencies.objects.get(id=existing_user_competency_id, user=request.user.id, job_role_related=False)
    if not user_competency_object.skill.team:
        user_competency = UserCompetencies.objects.get(id=existing_user_competency_id,user=request.user.id)
        form_user_skill = UserSkillDefinitionForm(initial={'user_skill_definition': user_competency.skill.name})
        form_user_skill_level = UserSkillLevelForm(initial={'user_skill_level': user_competency.skill_level.name})
    else:
        user_competency = UserCompetencies.objects.get(id=existing_user_competency_id,user=request.user.id)
        form_user_skill_level = UserSkillLevelForm(initial={'user_skill_level': user_competency.skill_level.name})
    existing_user_competency_id = int(existing_user_competency_id)
    return {'form_user_skill': False if UserCompetencies.objects.get(id=existing_user_competency_id, user=request.user.id, job_role_related=False).skill.team else form_user_skill, 'form_user_skill_level': form_user_skill_level,
            'existing_user_competency_id': existing_user_competency_id}


def populate_existing_user_competencies(request):
    user_competencies = UserCompetencies.objects.filter(user=request.user.id)
    disabled_choices = []
    for user_competency in user_competencies:
        if user_competency.skill.name:
            disabled_choices.append(user_competency.skill.name)
    return disabled_choices
