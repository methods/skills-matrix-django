from super_admin.models import Team


def get_team_choices():
    team_options = [(team.team_name, team.team_name) for team in Team.objects.all()]
    team_options.insert(0, ('', '--Select a team--'))
    return team_options
