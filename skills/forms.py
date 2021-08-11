from django import forms
from common.widgets import GdsStyleTextInput
from common.widgets import CustomisedSelectWidget
from skills.form_utils import get_team_choices
from skills.models import Skill
from super_admin.models import Team


class SkillForm(forms.Form):
    skill_name = forms.CharField(label="Skill name", max_length=100,
                                           widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                           error_messages={'required': 'Enter the name of the skill'})

    skill_description = forms.CharField(label="Skill description (optional)", max_length=400,
                                           widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                           required=False)

    team = forms.ChoiceField(choices=[], widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'},
                                                                       disabled_choices=['']))

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.fields['team'].choices = get_team_choices()
        attrs = {}
        attrs.update({"errors": True})
        for field in self.fields:
            if field in self.errors and field == 'skill_name':
                attrs['class'] = 'govuk-input--error'
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)
            if field in self.errors and field == 'team':
                attrs['class'] = 'govuk-select govuk-select--error'
                self.fields[field].widget.attrs = attrs

    def process(self):
        skill_name = self.cleaned_data['skill_name']
        skill_description = self.cleaned_data['skill_description'] or ''
        team = Team.objects.get(team_name=self.cleaned_data['team'])
        Skill.objects.create(name=skill_name, description=skill_description, team=team)

