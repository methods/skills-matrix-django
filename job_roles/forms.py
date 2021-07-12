from django import forms
from signup.widgets import GdsStyleTextInput


class JobTitleForm(forms.Form):
    job_role_title = forms.CharField(label="Enter a new job title, e.g. 'Junior Developer'.", max_length=100,
                                           widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                           error_messages={'required': 'Enter a job role title'})
