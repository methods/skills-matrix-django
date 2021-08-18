from app.forms import UserSkillLevelForm
from skills.models import UserCompetencies


def prepare_competency_update(individual_job_related_competency_id):
    individual_job_related_competency = UserCompetencies.objects.get(id=individual_job_related_competency_id)
    form = UserSkillLevelForm(initial={'user_skill_level': individual_job_related_competency.skill_level.name})
    update_indiviudal_competency_id = int(individual_job_related_competency_id)
    return {'form': form, 'update_indiviudal_competency_id': update_indiviudal_competency_id}
