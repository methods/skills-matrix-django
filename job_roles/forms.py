from django import forms
from signup.widgets import GdsStyleTextInput
from .validators import validate_input_capitalised


class JobTitleForm(forms.Form):
    job_role_title = forms.CharField(label="Enter a new job title, e.g. 'Junior Developer'.", max_length=100,
                                           validators=[validate_input_capitalised],
                                           widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                           error_messages={'required': 'Enter a job role title'})

    def __init__(self, *args, **kwargs):
        super(JobTitleForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)
