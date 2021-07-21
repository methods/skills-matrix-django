from django import forms
from signup.widgets import GdsStyleTextInput
from .widgets import CustomisedSelectWidget
from app.models import Skill, SkillLevel
from .validators import validate_input_capitalised
from .fields import EmptyChoiceField


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
    def get_skill_choices():
        skill_options = ((skill.name, skill.name) for skill in Skill.objects.all())
        return skill_options

    def get_skill_level_choices():
        skill_level_options = ((skill_level.name, skill_level.name) for skill_level in SkillLevel.objects.all())
        return skill_level_options

    job_role_skill = EmptyChoiceField(choices=get_skill_choices(), empty_label='--Select a skill--', required=False, widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'}))
    job_role_skill_level = forms.ChoiceField(choices=get_skill_level_choices,
                                             widget=forms.Select(attrs={'class': 'govuk-select'}))

    def __init__(self, *args, disabled_choices=None, **kwargs):
        super(JobSkillsAndSkillLevelForm, self).__init__(*args, **kwargs)
        if disabled_choices:
            self.fields['job_role_skill'].widget.disabled_choices = disabled_choices


class UpdateJobForm(JobSkillsAndSkillLevelForm, JobTitleForm):
    pass
