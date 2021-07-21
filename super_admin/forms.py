from django import forms
from common.widgets import GdsStylePasswordInput,GdsStyleTextInput,GdsStyleEmailInput


class SkillLevelForm(forms.Form):
    name = forms.CharField(label='Skill level', max_length=100,
                                 widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                           error_messages={'required': 'Enter name of skill level'})
    description = forms.CharField(label='Description (optional)', max_length=1000, required=False,
                              widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}))

    def __init__(self, *args, **kwargs):
        super(SkillLevelForm, self).__init__(*args, **kwargs)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)