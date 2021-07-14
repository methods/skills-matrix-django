from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from job_roles.forms import JobTitleForm, JobSkillsAndSkillLevelForm


@login_required
def job_roles(request):
    return render(request, "job_roles/job-roles.html", {"user": request.user})


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
                request.session['disabled_choices'].append(request.POST['job_role_skill'])
                request.session['new_added_job_competencies'].append({request.POST['job_role_skill']:
                                                                      request.POST['job_role_skill_level']})

            request.session.save()
            form = JobSkillsAndSkillLevelForm(disabled_choices=request.session['disabled_choices'])
            render(request, "job_roles/add_job_role_skills.html", {'form': form})
        else:
            print(form.errors)
    else:
        form = JobSkillsAndSkillLevelForm()
    return render(request, "job_roles/add_job_role_skills.html", {'form': form})


def new_job_role(request):
    pass
