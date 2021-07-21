from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm, UpdateJobForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Job, Competency
from app.models import Skill
from super_admin.models import SkillLevel


@login_required
def job_roles(request):
    if request.method == "GET":
        if 'job_role_title' in request.session.keys(): del request.session['job_role_title']
        if 'disabled_choices' in request.session.keys(): del request.session['disabled_choices']
        if 'new_added_job_competencies' in request.session.keys(): del request.session['new_added_job_competencies']
    job_list = []
    skill_list = Job.objects.all()
    for skill in skill_list:
        competencies = Competency.objects.filter(job_role_title=skill.id)
        for competency in competencies:
            job_list.append(competency.job_role_title.job_title)
    job_role_list = list(dict.fromkeys(job_list))
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
            render(request, "job_roles/add_job_role_skills.html", {'form': form})
            if "saveandcontinue" in request.POST.keys():
                return redirect(review_job_role)
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


def dynamic_job_role_lookup_view(request, job):
    job_title = Job.objects.get(job_title=job.title().replace('-', ' '))
    job_role_obj = Competency.objects.filter(job_role_title=job_title.id)
    return render(request, "job_roles/job_role_detail.html", {'job_role_obj': job_role_obj, 'job_title': job.title().replace('-', ' ')})


def update_job_role_detail_view(request, job_title):
    job_title = Job.objects.get(job_title=job_title.title().replace('-', ' '))
    job_role_obj = Competency.objects.filter(job_role_title=job_title.id)
    return render(request, "job_roles/update_job_role.html", {'job_role_obj': job_role_obj, 'job_title': job_title})









# def update_job_role_detail_view(request, job_title):
#     job_title = Job.objects.get(job_title=job_title.title().replace('-', ' '))
#     job_role_obj = Competency.objects.filter(job_role_title=job_title.id)
#     request.session['selected_skills'] = []
#     request.session['disabled_choices']=request.session['selected_skills']
#     form_list =[]
#     for job_role in job_role_obj:
#         request.session['selected_skills'].append(job_role.job_role_skill.name)
#     for competency in job_role_obj:
#         form_list.append(UpdateJobForm(initial={'job_role_title': job_title.job_title, 'job_role_skill': competency.job_role_skill.name,'job_role_skill_level': competency.job_role_skill_level.name}, disabled_choices=request.session['disabled_choices']))
#     print('post request', request.POST)
#     if request.method == 'POST':
#         print(request.POST)
#         form = UpdateJobForm(request.POST)
#         print('I am NOT valid')
#         if form.is_valid():
#             form_list = []
#             print('I am valid')
#             if 'deletejobroleskills' in request.POST.keys():
#                 job_role_obj = Competency.objects.filter(job_role_title=job_title.id)
#                 job_skill = Skill.objects.get(name=request.POST["deletejobroleskills"])
#                 print(job_skill.name)
#                 Competency.objects.get(job_role_skill=job_skill.id, job_role_title=job_title.id).delete()
#                 for existing_competency in job_role_obj:
#                     form_list.append(UpdateJobForm(initial={'job_role_title': request.POST['job_role_title'] if 'job_role_title' in request.POST.keys() else existing_competency.job_role_title.job_title, 'job_role_skill': request.POST['job_role_skill'] if 'job_role_skill' in request.POST.keys() else existing_competency.job_role_skill.name, 'job_role_skill_level': request.POST['job_role_skill_level'] if 'job_role_skill_level' in request.POST.keys() else existing_competency.job_role_skill_level.name}, disabled_choices=request.session['disabled_choices']))
#             return render(request, "job_roles/update_job_role.html", {'form_list': form_list})
#         return render(request, "job_roles/update_job_role.html", {'form_list': form_list})
#     return render(request, "job_roles/update_job_role.html", {'form_list': form_list})
