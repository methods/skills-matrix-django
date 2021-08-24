from django import forms
from common.widgets import CustomisedSelectWidget, GdsStyleTextInput
from job_roles.form_utils import get_skill_level_choices


class UserSkillLevelForm(forms.Form):
    user_skill_level = forms.ChoiceField(choices=[], required=False,
                                         widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'},
                                         disabled_choices=['']))

    def __init__(self, *args, **kwargs):
        super(UserSkillLevelForm, self).__init__(*args, **kwargs)
        self.fields['user_skill_level'].choices = get_skill_level_choices()

    def clean_job_role_skill_level(self):
        skill_level = self.cleaned_data.get('job_role_skill_level')
        if not skill_level:
            raise forms.ValidationError('Select a skill level')
        return skill_level


class UserSkillDefinitionForm(forms.Form):
    user_skill_definition = forms.CharField(label="Enter your skill, e.g. 'Project Management'.", max_length=100,
                                            widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                            error_messages={'required': 'Enter a skill'})

    def __init__(self, *args, **kwargs):
        super(UserSkillDefinitionForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)