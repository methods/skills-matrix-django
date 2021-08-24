from .models import Competency
from .forms import JobSkillsAndSkillLevelForm


def populate_existing_competencies(job, existing_competency=None):
    competencies = Competency.objects.filter(job_role_title=job.id)
    disabled_choices = ['']
    for competency in competencies:
        if existing_competency != competency.job_role_skill.name:
            disabled_choices.append(competency.job_role_skill.name)
    return disabled_choices


def prepare_competency_edit(competency_id, job_title):
    competency = Competency.objects.get(id=competency_id)
    disabled_choices = populate_existing_competencies(job_title, competency.job_role_skill.name)
    form = JobSkillsAndSkillLevelForm(initial={'job_role_skill': competency.job_role_skill.name,
                                               'job_role_skill_level': competency.job_role_skill_level.name},
                                      disabled_choices=disabled_choices)
    edit_competency_id = int(competency_id)
    return {'form': form, 'edit_competency_id': edit_competency_id}



