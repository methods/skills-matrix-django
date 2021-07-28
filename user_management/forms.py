from django import forms
from common.widgets import GdsStylePasswordInput, GdsStyleTextInput, GdsStyleEmailInput
from .validators import validate_domain_email
from .utils import get_job_choices, get_team_choices


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


class JobForm(forms.Form):

    team = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'govuk-select'}))
    job = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'govuk-select'}))

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['team'].choices = get_team_choices()
        self.fields['job'].choices = get_job_choices()


class EmailForm(forms.Form):
    email_address = forms.EmailField(validators=[validate_domain_email], label='Email address', max_length=100,
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