from django import forms
from common.widgets import GdsStylePasswordInput, GdsStyleTextInput, GdsStyleEmailInput, CustomisedSelectWidget
from .validators import validate_domain_email
from .utils import get_job_choices, get_team_choices
from django.contrib.auth.hashers import make_password


class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                 error_messages={'required': 'Enter your first name'})
    surname = forms.CharField(label='Surname', max_length=100,
                              widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                              error_messages={'required': 'Enter your surname'})

    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)

    def process_in_signup(self, request):
        request.session['first_name'] = request.POST['first_name']
        request.session['surname'] = request.POST['surname']
        request.session.save()


class JobForm(forms.Form):

    team = forms.ChoiceField(choices=[], required=False, widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'},
                                                                       disabled_choices=['']))
    job_role = forms.ChoiceField(choices=[], required=False, widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'},
                                                                      disabled_choices=['']))

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['team'].choices = get_team_choices()
        self.fields['job_role'].choices = get_job_choices()
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-select govuk-select--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget.attrs = attrs

    def clean_team(self):
        team = self.cleaned_data.get('team')
        if not team:
            raise forms.ValidationError('Select a team')
        return team

    def clean_job_role(self):
        job = self.cleaned_data.get('job_role')
        if not job:
            raise forms.ValidationError('Select a job')
        return job

    def process_in_signup(self, request):
        request.session['team'] = request.POST['team']
        request.session['job'] = request.POST['job_role']
        request.session.save()


class EmailForm(forms.Form):
    email = forms.EmailField(validators=[validate_domain_email], label='Email address', max_length=100,
                                     widget=GdsStyleEmailInput(attrs={'class': 'govuk-input'}),
                                     error_messages={'required': 'Enter your email address.',
                                     'invalid': "Enter an email address in the correct format, like name@example.com"})

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleEmailInput(attrs=attrs)

    def process_in_signup(self, request):
        request.session['email_address'] = request.POST['email']
        request.session.save()


class PasswordForm(forms.Form):
    password = forms.CharField(widget=GdsStylePasswordInput(),
                               label='You will use this password to log in securely to the platform.',
                               min_length=8, max_length=25,
                               error_messages={'required': 'Enter your password'})
    password_confirm = forms.CharField(widget=GdsStylePasswordInput(), label='Confirm password', min_length=8,
                                       max_length=25,
                                       error_messages={'required': 'Confirm your password'})

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
        if self.errors:
            for field in self.fields:
                self.fields[field].widget = GdsStylePasswordInput(attrs=attrs)

    def process(self, request):
        password = request.POST['password']
        hashed_password = make_password(password)
        request.session['hashed_password'] = hashed_password
        request.session.save()
