from .models import Competency
from .forms import JobSkillsAndSkillLevelForm
from django.contrib import messages
from skills.models import Skill
from super_admin.models import SkillLevel


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


def set_disabled_choices_to_empty_string_list(request):
    if 'disabled_choices' not in request.session.keys():
        request.session['disabled_choices'] = ['']
        return


def handle_form_errors(form, request):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, error)


def create_competencies(new_competencies, job_title):
    for key, value in new_competencies.items():
        job_role_skill = Skill.objects.get(name=key)
        job_role_skill_level = SkillLevel.objects.get(name=value)
        Competency(job_role_title=job_title, job_role_skill=job_role_skill,
                   job_role_skill_level=job_role_skill_level).save()