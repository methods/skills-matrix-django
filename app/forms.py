from django import forms
from common.widgets import CustomisedSelectWidget
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
