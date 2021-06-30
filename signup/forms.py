from django import forms
from django.apps import apps
from django.forms.widgets import PasswordInput
from signup.widgets import GdsStyleInput


class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'govuk-input'}))
    surname = forms.CharField(label='Surname', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'govuk-input'}))


class JobForm(forms.Form):
    team = forms.ChoiceField(widget=forms.Select(attrs={'class': 'govuk-select'}))
    job = forms.ChoiceField(widget=forms.Select(attrs={'class': 'govuk-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Team = apps.get_model('super_admin', 'Team')
        Job = apps.get_model('admin_user', 'Job')
        self.fields['team'].choices = [(team.team_name, team.team_name) for team in Team.objects.all()]
        self.fields['job'].choices = [(job.job_title, job.job_title) for job in Job.objects.all()]


class EmailForm(forms.Form):
    email_address = forms.EmailField(label='Email address', max_length=100,
                                     widget=forms.TextInput(attrs={'class': 'govuk-input'}))


class PasswordForm(forms.Form):
    password = forms.CharField(widget=GdsStyleInput(), label='You will use this password to '
                                                             'log in securely to the platform.',
                               min_length=8, max_length=25, error_messages={'required': 'Please Enter Your Password'})
    password_confirm = forms.CharField(widget=GdsStyleInput(), label='Confirm password',min_length=8, max_length=25,
                                       error_messages={'required': 'Please Confirm Your Password'})

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords must match')
        return password_confirm
    
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:  
                self.fields[field].widget = GdsStyleInput(attrs=attrs)