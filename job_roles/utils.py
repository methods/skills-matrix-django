from .models import Competency


def populate_existing_competencies(job):
    competencies = Competency.objects.filter(job_role_title=job.id)
    disabled_choices = []
    for competency in competencies:
        disabled_choices.append(competency.job_role_skill.name)
    return disabled_choices
