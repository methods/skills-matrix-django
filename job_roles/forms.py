from django import forms
from common.widgets import GdsStyleTextInput
from .widgets import CustomisedSelectWidget
from .validators import validate_input_capitalised
from .fields import EmptyChoiceField
from .utils import get_skill_choices, get_skill_level_choices


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

    job_role_skill = EmptyChoiceField(choices=[], empty_label='--Select a skill--', required=False,
                                      widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'}))
    job_role_skill_level = forms.ChoiceField(choices=[],
                                             widget=forms.Select(attrs={'class': 'govuk-select'}))

    def __init__(self, *args, disabled_choices=None, **kwargs):
        super(JobSkillsAndSkillLevelForm, self).__init__(*args, **kwargs)
        self.fields['job_role_skill'].choices = get_skill_choices()
        self.fields['job_role_skill_level'].choices = get_skill_level_choices()
        if disabled_choices:
            self.fields['job_role_skill'].widget.disabled_choices = disabled_choices

