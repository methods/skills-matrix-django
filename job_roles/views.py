from django.shortcuts import render, redirect
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm
from django.contrib import messages
from .models import Job, Competency
from skills.models import Skill
from super_admin.models import SkillLevel
from django.utils.text import slugify
from common.custom_class_view import CustomView
from common.user_group_check_mixins import AdminUserMixin, CustomLoginRequiredMixin


class JobRoles(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        if 'job_role_title' in request.session.keys(): del request.session['job_role_title']
        if 'disabled_choices' in request.session.keys(): del request.session['disabled_choices']
        if 'new_added_job_competencies' in request.session.keys(): del request.session['new_added_job_competencies']
        job_role_list = Job.objects.all().order_by('id')
        return render(request, "job_roles/job-roles.html", {"user": request.user, 'job_role_list': job_role_list})


class AddJobRole(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def get(self, request):
        form = JobTitleForm(request=request)
        form.fields['job_role_title'].initial = request.session[
            'job_role_title'] if 'job_role_title' in request.session else ''
        return render(request, "job_roles/add_job_role.html", {'form': form})

    def post(self, request):
        form = JobTitleForm(request.POST, request=request)
        if form.is_valid():
            form.process_session_save()
            return redirect('add-job-skills')
        return render(request, "job_roles/add_job_role.html", {'form': form})


class AddJobRoleSkills(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def set_disabled_choices_to_empty_string_list(self, request):
        if 'disabled_choices' not in request.session.keys():
            request.session['disabled_choices'] = ['']

    def get(self, request):
        if 'job_role_title' in request.session.keys():
            self.set_disabled_choices_to_empty_string_list(request)
            form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
            competencies = request.session[
                'new_added_job_competencies'] if 'new_added_job_competencies' in request.session.keys() else []
            return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies,
                                                                          'new_role': True})
        else:
            messages.info(request, 'Please make sure to add a job role title.')
            return redirect('add-job-title')

    def post(self, request):
        if 'job_role_title' in request.session.keys():
            self.set_disabled_choices_to_empty_string_list(request)
        form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=request.session['disabled_choices'],
                                              request=request)
        if 'new_added_job_competencies' not in request.session.keys():
            request.session['new_added_job_competencies'] = []
        if 'addSkill' in request.POST.keys():
            if form.is_valid():
                form.process_session_save()
                form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
            else:
                self.handle_form_errors(form, request)
            competencies = request.session[
                'new_added_job_competencies'] if 'new_added_job_competencies' in request.session.keys() else []
            return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies,
                                                                          'new_role': True})

    def delete(self, request):
        form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
        if request.POST["delete"] in request.session['disabled_choices'] and len(
                request.session['disabled_choices']) > 0:
            request.session['disabled_choices'].remove(request.POST['delete'])
        for competency in request.session['new_added_job_competencies']:
            if request.POST["delete"] in competency:
                request.session['new_added_job_competencies'].remove(competency)
        competencies = request.session[
            'new_added_job_competencies'] if 'new_added_job_competencies' in request.session.keys() else []
        return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies,
                                                                      'new_role': True})


class ReviewJobRole(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def create_competency(self, new_competencies, job_title):
        for key, value in new_competencies.items():
            job_role_skill = Skill.objects.get(name=key)
            job_role_skill_level = SkillLevel.objects.get(name=value)
            Competency(job_role_title=job_title, job_role_skill=job_role_skill,
                       job_role_skill_level=job_role_skill_level).save()

    def get(self, request):
        if 'job_role_title' and 'new_added_job_competencies' in request.session.keys():
            if len(request.session['new_added_job_competencies']) == 0:
                messages.info(request, 'Please make sure to add the relevant skills to this job role.')
                return redirect('add-job-skills')
        elif 'job_role_title' not in request.session.keys():
            messages.info(request, 'Please make sure to add a job role title.')
            return redirect('add-job-title')
        elif 'new_added_job_competencies' not in request.session.keys():
            messages.info(request, 'Please make sure to add the relevant skills to this job role.')
            return redirect('add-job-skills')
        return render(request, "job_roles/review_job_role.html")

    def post(self, request):
        job_title = request.session['job_role_title']
        Job(job_title=job_title).save()
        job_role_title = Job.objects.get(job_title=job_title)
        for new_job_competencies in request.session['new_added_job_competencies']:
            self.create_competency(new_job_competencies, job_role_title)
        messages.success(request, 'The new job role was added successfully.')
        return redirect('job-roles')


class DynamicJobRoleLookup(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def get(self, request, job):
        job_title = Job.objects.get(job_title=job.title().replace('-', ' '))
        job_role_obj = Competency.objects.filter(job_role_title=job_title.id)
        return render(request, "job_roles/job_role_detail.html", {'job_role_obj': job_role_obj, 'job_title': job_title})


class UpdateJobRoleDetail(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def prepare_competency_edit(self, competency_id, job_title):
        competency = Competency.objects.get(id=competency_id)
        disabled_choices = self.populate_existing_competencies(job_title, competency.job_role_skill.name)
        form = JobSkillsAndSkillLevelForm(initial={'job_role_skill': competency.job_role_skill.name,
                                                   'job_role_skill_level': competency.job_role_skill_level.name},
                                          disabled_choices=disabled_choices)
        edit_competency_id = int(competency_id)
        return form, edit_competency_id

    def get(self, request, job_title):
        job, competencies = self.set_job_and_competencies(job_title)
        return render(request, "job_roles/update_job_role.html", {'competencies': competencies,
                                                                  'job_title': job, 'form_job_role_title': False})

    def edit(self, request, job_title):
        job, competencies = self.set_job_and_competencies(job_title)
        if 'edit_competency' in request.POST.keys():
            form, edit_competency_id = self.prepare_competency_edit(request.POST['edit_competency'], job)
            return render(request, "job_roles/update_job_role.html", {'competencies': competencies, 'job_title': job,
                                                                      'form': form,
                                                                      'edit_competency_id': edit_competency_id})
        if 'update_competency' in request.POST.keys():
            disabled_choices = self.populate_existing_competencies(job)
            form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=disabled_choices)
            if form.is_valid():
                form.process(request.POST)
        if 'edit_job_role_title' in request.POST.keys():
            form_job_role_title = JobTitleForm(initial={'job_role_title': job.job_title})
            return render(request, "job_roles/update_job_role.html",
                          {'form_job_role_title': form_job_role_title, 'job_title': job,
                           'competencies': competencies
                           })

    def post(self, request, job_title):
        job, competencies = self.set_job_and_competencies(job_title)
        if 'save_competency' in request.POST.keys():
            disabled_choices = self.populate_existing_competencies(job)
            form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=disabled_choices)
            if form.is_valid():
                form.process(request.POST)

        if 'save_job_role_title' in request.POST.keys():
            form_job_role_title = JobTitleForm(request.POST)
            if form_job_role_title.is_valid():
                updated_title = form_job_role_title.process_edit(request.POST['save_job_role_title'])
                return redirect('update-job-role-view', job_title=slugify(updated_title))
        return render(request, "job_roles/update_job_role.html", {'competencies': competencies,
                                                                  'job_title': job, 'form_job_role_title': False if
                                            'save_job_role_title' not in request.POST.keys() else form_job_role_title})

    def delete(self, request, job_title):
        job, competencies = self.set_job_and_competencies(job_title)
        Competency.objects.get(id=request.POST['delete']).delete()
        return render(request, "job_roles/update_job_role.html", {'competencies': competencies, 'job_title': job,
                                                                    'form_job_role_title': False})


class DeleteJobRole(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def get(self, request, job_title):
        job = Job.objects.get(job_title=job_title.title().replace('-', ' '))
        return render(request, "job_roles/delete_job_role.html", {'job_title': job})

    def delete(self, request, job_title):
        job = Job.objects.get(job_title=job_title.title().replace('-', ' '))
        Job.objects.get(id=request.POST['delete']).delete()
        return render(request, "job_roles/delete_job_role_confirmation.html", {'job_title': job})


class AddASkill(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def create_competencies_list(self, job_title):
        _, competencies_by_id = self.set_job_and_competencies(job_title)
        competencies_by_name = []
        for competency in competencies_by_id:
            skill = Skill.objects.filter(id=competency.job_role_skill.id)
            skill_level = SkillLevel.objects.filter(id=competency.job_role_skill_level.id)
            competencies_by_name.append({skill[0].name: skill_level[0].name})
        return competencies_by_name

    def get(self, request, job_title):
        job, _ = self.set_job_and_competencies(job_title)
        disabled_choices = self.populate_existing_competencies(job)
        form = JobSkillsAndSkillLevelForm(disabled_choices=disabled_choices)
        competencies_by_name = self.create_competencies_list(job_title)
        return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies_by_name
                                                                , 'job_title': job.job_title, 'existing_role': True})

    def post(self, request, job_title):
        job, _ = self.set_job_and_competencies(job_title)
        disabled_choices = self.populate_existing_competencies(job)
        form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=disabled_choices, request=request)
        if form.is_valid():
            form.process(request.POST, job)
            return redirect('add-a-skill', job_title=job_title)
        else:
            self.handle_form_errors(form, request)
            competencies_by_name = self.create_competencies_list(job_title)
            return render(request, "job_roles/add_job_role_skills.html",
                          {'form': form, 'competencies': competencies_by_name,
                           'job_title': job.job_title, 'existing_role': True})

