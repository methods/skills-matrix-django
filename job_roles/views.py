from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Job, Competency
from app.models import Skill
from super_admin.models import SkillLevel
from .utils import populate_existing_competencies
from django.utils.text import slugify


@login_required
def job_roles(request):
    if request.method == "GET":
        if 'job_role_title' in request.session.keys(): del request.session['job_role_title']
        if 'disabled_choices' in request.session.keys(): del request.session['disabled_choices']
        if 'new_added_job_competencies' in request.session.keys(): del request.session['new_added_job_competencies']
    job_role_list = Job.objects.all().order_by('id')
    return render(request, "job_roles/job-roles.html", {"user": request.user, 'job_role_list': job_role_list})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def add_job_role(request):
    if request.method == 'POST':
        form = JobTitleForm(request.POST)
        if form.is_valid():
            request.session['job_role_title'] = request.POST['job_role_title']
            request.session.save()
            return redirect(add_job_role_skills)
    else:
        form = JobTitleForm()
        form.fields['job_role_title'].initial = request.session['job_role_title'] if 'job_role_title' in request.session else ''
    return render(request, "job_roles/add_job_role.html", {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def add_job_role_skills(request):
    if request.method == 'POST':
        if 'disabled_choices' in request.session.keys():
            form = JobSkillsAndSkillLevelForm(request.POST, disabled_choices=request.session['disabled_choices'])
        else:
            form = JobSkillsAndSkillLevelForm(request.POST)
            request.session['disabled_choices'] = []
        if 'new_added_job_competencies' not in request.session.keys():
            request.session['new_added_job_competencies'] = []
        if form.is_valid():
            if "saveandcontinue" in request.POST.keys():
                return redirect(review_job_role)
            if 'delete' in request.POST.keys():
                if request.POST["delete"] in request.session['disabled_choices'] and len(request.session['disabled_choices']) > 0:
                    request.session['disabled_choices'].remove(request.POST['delete'])
                for competency in request.session['new_added_job_competencies']:
                    if request.POST["delete"] in competency:
                        request.session['new_added_job_competencies'].remove(competency)
                form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
            if 'addSkill' in request.POST.keys():
                job_role_skill = form.cleaned_data['job_role_skill']
                if not job_role_skill:
                    raise ValidationError('Select a valid option')
                else:
                    request.session['disabled_choices'].append(request.POST['job_role_skill'])
                    request.session['new_added_job_competencies'].append({request.POST['job_role_skill']:
                                                                          request.POST['job_role_skill_level']})
            request.session.save()
            form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
            competencies = request.session['new_added_job_competencies']
            return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies,
                                                                          'new_role': True})
    else:
        form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices']) if 'disabled_choices' in request.session.keys() else JobSkillsAndSkillLevelForm()
    return render(request, "job_roles/add_job_role_skills.html", {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def review_job_role(request):
    job_title = request.session['job_role_title']
    if request.method == 'POST':
        Job(job_title=job_title).save()
        job_role_title = Job.objects.get(job_title=job_title)
        for new_job_competencies in request.session['new_added_job_competencies']:
            for key, value in new_job_competencies.items():
                job_role_skill = Skill.objects.get(name=key)
                job_role_skill_level = SkillLevel.objects.get(name=value)
                Competency(job_role_title=job_role_title, job_role_skill=job_role_skill, job_role_skill_level=job_role_skill_level).save()
        messages.success(request, 'The new job role was added successfully.')
        return redirect(job_roles)
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
            competency = Competency.objects.get(id=request.POST['edit_competency'])
            disabled_choices = populate_existing_competencies(job_title, competency.job_role_skill.name)
            form = JobSkillsAndSkillLevelForm(initial={'job_role_skill': competency.job_role_skill.name,
                                                       'job_role_skill_level': competency.job_role_skill_level.name},
                                              disabled_choices=disabled_choices)
            edit_competency_id = int(request.POST['edit_competency'])
            return render(request, "job_roles/update_job_role.html", {'job_role_obj': job_role_obj,
                                                                      'job_title': job_title,
                                                                      'form': form,
                                                                      'edit_competency_id': edit_competency_id})
        if 'update_competency' in request.POST.keys():
            form = JobSkillsAndSkillLevelForm(request.POST)
            if form.is_valid():
                competency = Competency.objects.get(id=request.POST['update_competency'])
                competency.job_role_skill = Skill.objects.get(name=request.POST['job_role_skill'])
                competency.job_role_skill_level = SkillLevel.objects.get(name=request.POST['job_role_skill_level'])
                competency.save()
        if 'edit_job_role_title' in request.POST.keys():
            form_job_role_title = JobTitleForm(initial={'job_role_title': job_title.job_title})
            return render(request, "job_roles/update_job_role.html", {'form_job_role_title': form_job_role_title, 'job_title': job_title, 'job_role_obj': job_role_obj
                                                                      })
        if 'save_job_role_title' in request.POST.keys():
            form_job_role_title = JobTitleForm(request.POST)
            if form_job_role_title.is_valid():
                updated_title = form_job_role_title.cleaned_data['job_role_title']
                Job.objects.filter(id=request.POST['save_job_role_title']).update(job_title=updated_title)
                return redirect(update_job_role_detail_view, job_title=slugify(updated_title))
    return render(request, "job_roles/update_job_role.html", {'job_role_obj': job_role_obj, 'job_title': job_title})


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
    if request.POST:
        job_role_skill = Skill.objects.get(name=request.POST['job_role_skill'])
        job_role_skill_level = SkillLevel.objects.get(name=request.POST['job_role_skill_level'])
        Competency(job_role_title=job, job_role_skill=job_role_skill,
                   job_role_skill_level=job_role_skill_level).save()
        return redirect(update_job_role_detail_view, job_title=job_title)
    else:
        disabled_choices = populate_existing_competencies(job)
        form = JobSkillsAndSkillLevelForm(disabled_choices=disabled_choices) if 'disabled_choices' != [] else JobSkillsAndSkillLevelForm()
        competencies_by_id = Competency.objects.filter(job_role_title=job.id)
        competencies_by_name = []
        for competency in competencies_by_id:
            skill = Skill.objects.filter(id=competency.job_role_skill.id)
            skill_level = SkillLevel.objects.filter(id=competency.job_role_skill_level.id)
            competencies_by_name.append({skill[0].name: skill_level[0].name})
        return render(request, "job_roles/add_job_role_skills.html", {'form': form, 'competencies': competencies_by_name, 'job_title': job.job_title})
