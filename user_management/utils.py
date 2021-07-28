from super_admin.models import Team
from job_roles.models import Job


def get_team_choices():
    team_options = [(team.team_name, team.team_name) for team in Team.objects.all()]
    return team_options


def get_job_choices():
    job_options = [(job.job_title, job.job_title) for job in Job.objects.all()]
    return job_options