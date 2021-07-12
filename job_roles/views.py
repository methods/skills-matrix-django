from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from job_roles.forms import JobTitleForm


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


def add_job_role_skills(request):
    return render(request, "job_roles/add_job_role_skills.html")
