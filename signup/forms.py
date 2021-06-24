from django import forms
from django.apps import apps


class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    surname = forms.CharField(label='Surname', max_length=100)


class JobForm(forms.Form):
    team = forms.ChoiceField(widget=forms.Select(attrs={'class': 'govuk-select'}))
    job = forms.ChoiceField(widget=forms.Select(attrs={'class': 'govuk-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Team = apps.get_model('super_admin', 'Team')
        Job = apps.get_model('admin_user', 'Job')
        self.fields['team'].choices = [(team.team_name, team.team_name) for team in Team.objects.all()]
        self.fields['job'].choices = [(job.job_title, job.job_title) for job in Job.objects.all()]
