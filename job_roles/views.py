from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm
from django.contrib import messages
from .models import Job, Competency
from skills.models import Skill
from super_admin.models import SkillLevel
from .view_utils import populate_existing_competencies
from django.utils.text import slugify
from .view_utils import prepare_competency_edit
from common.custom_class_view import CustomView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.user_group_check_mixins import AdminUserMixin


class JobRoles(LoginRequiredMixin, CustomView):
    def get(self, request):
        if 'job_role_title' in request.session.keys(): del request.session['job_role_title']
        if 'disabled_choices' in request.session.keys(): del request.session['disabled_choices']
        if 'new_added_job_competencies' in request.session.keys(): del request.session['new_added_job_competencies']
        job_role_list = Job.objects.all().order_by('id')
        return render(request, "job_roles/job-roles.html", {"user": request.user, 'job_role_list': job_role_list})


class AddJobRole(LoginRequiredMixin, AdminUserMixin, CustomView):
    def get(self, request):
        form = JobTitleForm(request=request)
        form.fields['job_role_title'].initial = request.session[
            'job_role_title'] if 'job_role_title' in request.session else ''
        return render(request, "job_roles/add_job_role.html", {'form': form})

    def post(self, request):
        form = JobTitleForm(request.POST, request=request)
        if form.is_valid():
            form.process_session_save()
            return redirect(add_job_role_skills)
        return render(request, "job_roles/add_job_role.html", {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def add_job_role_skills(request):
    if 'job_role_title' in request.session.keys():
        if 'disabled_choices' not in request.session.keys():
            request.session['disabled_choices'] = ['']
        form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
    else:
        messages.info(request, 'Please make sure to add a job role title.')
        return redirect('add-job-title')
    if request.method == 'POST':
        if 'delete' in request.POST.keys():
            if request.POST["delete"] in request.session['disabled_choices'] and len(
                    request.session['disabled_choices']) > 0:
                request.session['disabled_choices'].remove(request.POST['delete'])
            for competency in request.session['new_added_job_competencies']:
                if request.POST["delete"] in competency:
                    request.session['new_added_job_competencies'].remove(competency)
        else:
            if 'disabled_choices' in request.session.keys():
                form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=request.session['disabled_choices'], request=request)
            else:
                form = JobSkillsAndSkillLevelForm(request.POST, request=request)
            if 'new_added_job_competencies' not in request.session.keys():
                request.session['new_added_job_competencies'] = []
            if 'addSkill' in request.POST.keys():
                if form.is_valid():
                    form.process_session_save()
                    form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, error)
    competencies = request.session['new_added_job_competencies'] if 'new_added_job_competencies' in request.session.keys() else []
    return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies,
                                                                  'new_role': True})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def review_job_role(request):
    if 'job_role_title' and 'new_added_job_competencies' in request.session.keys():
        job_title = request.session['job_role_title']
        if len(request.session['new_added_job_competencies']) == 0:
            messages.info(request, 'Please make sure to add the relevant skills to this job role.')
            return redirect(add_job_role_skills)
    elif 'job_role_title' not in request.session.keys():
        messages.info(request, 'Please make sure to add a job role title.')
        return redirect('add-job-title')
    elif 'new_added_job_competencies' not in request.session.keys():
        messages.info(request, 'Please make sure to add the relevant skills to this job role.')
        return redirect(add_job_role_skills)
    if request.method == 'POST':
        Job(job_title=job_title).save()
        job_role_title = Job.objects.get(job_title=job_title)
        for new_job_competencies in request.session['new_added_job_competencies']:
            for key, value in new_job_competencies.items():
                job_role_skill = Skill.objects.get(name=key)
                job_role_skill_level = SkillLevel.objects.get(name=value)
                Competency(job_role_title=job_role_title, job_role_skill=job_role_skill, job_role_skill_level=job_role_skill_level).save()
        messages.success(request, 'The new job role was added successfully.')
        return redirect('job-roles')
    return render(request, "job_roles/review_job_role.html")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def dynamic_job_role_lookup_view(request, job):
    job_title = Job.objects.get(job_title=job.title().replace('-', ' '))
    job_role_obj = Competency.objects.filter(job_role_title=job_title.id)
    return render(request, "job_roles/job_role_detail.html", {'job_role_obj': job_role_obj, 'job_title': job_title})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def update_job_role_detail_view(request, job_title):
    job_title = Job.objects.get(job_title=job_title.title().replace('-', ' '))
    job_role_obj = Competency.objects.filter(job_role_title=job_title.id).order_by('id')
    if request.method == 'POST':
        if 'delete_competency' in request.POST.keys():
            Competency.objects.get(id=request.POST['delete_competency']).delete()
        if 'edit_competency' in request.POST.keys():
            template_variables = prepare_competency_edit(request.POST['edit_competency'], job_title)
            return render(request, "job_roles/update_job_role.html", {'job_role_obj': job_role_obj,
                                                                      'job_title': job_title,
                                                                      'form': template_variables['form'],
                                                                      'edit_competency_id': template_variables['edit_competency_id']})
        if 'update_competency' in request.POST.keys():
            disabled_choices = populate_existing_competencies(job_title)
            form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=disabled_choices)
            if form.is_valid():
                form.process(request.POST)
        if 'edit_job_role_title' in request.POST.keys():
            form_job_role_title = JobTitleForm(initial={'job_role_title': job_title.job_title})
            return render(request, "job_roles/update_job_role.html", {'form_job_role_title': form_job_role_title, 'job_title': job_title, 'job_role_obj': job_role_obj
                                                                      })
        if 'save_job_role_title' in request.POST.keys():
            form_job_role_title = JobTitleForm(request.POST)
            if form_job_role_title.is_valid():
                updated_title = form_job_role_title.process_edit(request.POST['save_job_role_title'])
                return redirect(update_job_role_detail_view, job_title=slugify(updated_title))
    return render(request, "job_roles/update_job_role.html", {'job_role_obj': job_role_obj, 'job_title': job_title,'form_job_role_title': False if 'save_job_role_title' not in request.POST.keys() else form_job_role_title})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def delete_job_role_title_view(request, job_title):
    job_title = Job.objects.get(job_title=job_title.title().replace('-', ' '))
    if request.method == 'POST':
        if "delete_job_role" in request.POST.keys():
            Job.objects.get(id=request.POST['delete_job_role']).delete()
            return render(request, "job_roles/delete_job_role_confirmation.html", {'job_title': job_title})
    return render(request, "job_roles/delete_job_role.html", {'job_title': job_title})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def add_a_skill(request, job_title):
    job = Job.objects.get(job_title=job_title.title().replace('-', ' '))
    disabled_choices = populate_existing_competencies(job)
    form = JobSkillsAndSkillLevelForm(disabled_choices=disabled_choices) if 'disabled_choices' != [] else JobSkillsAndSkillLevelForm()
    competencies_by_id = Competency.objects.filter(job_role_title=job.id)
    competencies_by_name = []
    for competency in competencies_by_id:
        skill = Skill.objects.filter(id=competency.job_role_skill.id)
        skill_level = SkillLevel.objects.filter(id=competency.job_role_skill_level.id)
        competencies_by_name.append({skill[0].name: skill_level[0].name})
    if request.POST:
        form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=disabled_choices, request=request)
        if form.is_valid():
            form.process(request.POST, job)
            return redirect(add_a_skill, job_title=job_title)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies_by_name,
                                                                  'job_title': job.job_title, 'existing_role': True})
