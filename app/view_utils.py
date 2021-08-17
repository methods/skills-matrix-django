from job_roles.models import Competency
from app.forms import UserSkillLevelForm


def prepare_competency_update(competency_id):
    competency = Competency.objects.get(id=competency_id)
    form = UserSkillLevelForm(initial={'user_skill_level': competency.job_role_skill_level.name})
    update_competency_id = int(competency_id)
    return {'form': form, 'update_competency_id': update_competency_id}
