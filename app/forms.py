from django import forms
from common.widgets import CustomisedSelectWidget, GdsStyleTextInput
from job_roles.form_utils import get_skill_level_choices
from app.form_utils import get_all_available_skills
from app.widgets import GdsStyleTextarea


class UserSkillLevelForm(forms.Form):
    user_skill_level = forms.ChoiceField(choices=[], required=False,
                                         widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'},
                                         disabled_choices=['']))

    def __init__(self, *args, **kwargs):
        super(UserSkillLevelForm, self).__init__(*args, **kwargs)
        self.fields['user_skill_level'].choices = get_skill_level_choices()
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-select govuk-select--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget.attrs = attrs

    def clean_user_skill_level(self):
        skill_level = self.cleaned_data.get('user_skill_level')
        if not skill_level:
            raise forms.ValidationError('Select a skill level')
        return skill_level


class UserSkillDefinitionForm(forms.Form):
    user_skill_definition = forms.CharField(label="Enter your skill, e.g. 'Project Management'.", max_length=100,
                                            widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                            error_messages={'required': 'Enter a skill name'})

    def __init__(self, *args, **kwargs):
        super(UserSkillDefinitionForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)


class UserSkillForm(forms.Form):
    user_skill = forms.ChoiceField(choices=[], required=False,
                                   widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'}))

    def __init__(self, *args,disabled_choices=None, **kwargs):
        super(UserSkillForm, self).__init__(*args, **kwargs)
        self.fields['user_skill'].choices = get_all_available_skills()
        if disabled_choices:
            self.fields['user_skill'].widget.disabled_choices = disabled_choices
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-select govuk-select--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget.attrs = attrs

    def clean_user_skill(self):
        user_skill = self.cleaned_data.get('user_skill')
        if not user_skill:
            raise forms.ValidationError('Select a skill')
        return user_skill


class CreateUserSkillForm(UserSkillDefinitionForm, forms.Form):
    skill_description = forms.CharField(label="Skill description (optional)", max_length=400,
                                        widget=GdsStyleTextarea,
                                        required=False)

