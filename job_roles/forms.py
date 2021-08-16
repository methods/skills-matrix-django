from django import forms
from common.widgets import GdsStyleTextInput
from common.widgets import CustomisedSelectWidget
from .validators import validate_input_capitalised
from .form_utils import get_skill_choices, get_skill_level_choices
from .models import Job, Competency
from skills.models import Skill
from super_admin.models import SkillLevel


class JobTitleForm(forms.Form):
    job_role_title = forms.CharField(label="Enter a job title, e.g. 'Junior Developer'.", max_length=100,
                                           validators=[validate_input_capitalised],
                                           widget=GdsStyleTextInput(attrs={'class': 'govuk-input'}),
                                           error_messages={'required': 'Enter a job role title'})

    def __init__(self, *args, request=None, **kwargs):
        super(JobTitleForm, self).__init__(*args, **kwargs)
        if request:
            self.request = request
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleTextInput(attrs=attrs)

    def process_session_save(self):
        self.request.session['job_role_title'] = self.request.POST['job_role_title']
        self.request.session.save()

    def process_edit(self, pk):
        updated_title = self.cleaned_data['job_role_title']
        Job.objects.filter(id=pk).update(job_title=updated_title)
        return updated_title


class JobSkillsAndSkillLevelForm(forms.Form):

    job_role_skill = forms.ChoiceField(choices=[], required=False,
                                    widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'}))

    job_role_skill_level = forms.ChoiceField(choices=[],
                                             required=False,
                                             widget=CustomisedSelectWidget(attrs={'class': 'govuk-select'},
                                                                 disabled_choices=['']))

    def __init__(self, *args, disabled_choices=None, request=None, **kwargs):
        super(JobSkillsAndSkillLevelForm, self).__init__(*args, **kwargs)
        self.fields['job_role_skill'].choices = get_skill_choices()
        self.fields['job_role_skill_level'].choices = get_skill_level_choices()
        if disabled_choices:
            self.fields['job_role_skill'].widget.disabled_choices = disabled_choices
        if request:
            self.request = request
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-select govuk-select--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget.attrs = attrs

    def process_session_save(self):
        self.request.session['disabled_choices'].append(self.request.POST['job_role_skill'])
        self.request.session['new_added_job_competencies'].append({self.request.POST['job_role_skill']:
                                                                  self.request.POST['job_role_skill_level']})
        self.request.session.save()

    def process(self, request, job=None):
        job_role_skill = Skill.objects.get(name=request['job_role_skill'])
        job_role_skill_level = SkillLevel.objects.get(name=request['job_role_skill_level'])
        if job:
            Competency(job_role_title=job, job_role_skill=job_role_skill,
                       job_role_skill_level=job_role_skill_level).save()
        else:
            competency = Competency.objects.filter(id=request['update_competency'])
            competency.update(job_role_skill=job_role_skill,
                       job_role_skill_level=job_role_skill_level)

    def clean_job_role_skill(self):
        job_role_skill = self.cleaned_data.get('job_role_skill')
        if not job_role_skill:
            raise forms.ValidationError('Select a skill')
        return job_role_skill

    def clean_job_role_skill_level(self):
        skill_level = self.cleaned_data.get('job_role_skill_level')
        if not skill_level:
            raise forms.ValidationError('Select a skill level')
        return skill_level
