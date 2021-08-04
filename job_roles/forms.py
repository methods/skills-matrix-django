from django import forms
from common.widgets import GdsStyleTextInput
from common.widgets import CustomisedSelectWidget
from .validators import validate_input_capitalised
from .form_utils import get_skill_choices, get_skill_level_choices


class JobTitleForm(forms.Form):
    job_role_title = forms.CharField(label="Enter a job title, e.g. 'Junior Developer'.", max_length=100,
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


class JobSkillsAndSkillLevelForm(forms.Form):

    job_role_skill_level = forms.ChoiceField(choices=[],
                                             required=False,
                                             widget=forms.Select(attrs={'class': 'govuk-select'}))

    def __init__(self, *args, disabled_choices=None, **kwargs):
        super(JobSkillsAndSkillLevelForm, self).__init__(*args, **kwargs)
        self.fields['job_role_skill'] = forms.ChoiceField(choices=get_skill_choices(),
                                                         required=False,
                                                         widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'}))
        self.fields['job_role_skill_level'].choices = get_skill_level_choices()
        if disabled_choices:
            self.fields['job_role_skill'].widget.disabled_choices = disabled_choices
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-select govuk-select--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget.attrs = attrs

    def clean_job_role_skill(self):
        job_role_skill = self.cleaned_data.get('job_role_skill')
        if not job_role_skill:
            raise forms.ValidationError('Select a skill')
        return job_role_skill
