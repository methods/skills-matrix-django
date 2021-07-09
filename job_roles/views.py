from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required


@login_required
def job_roles(request):
    return render(request, "job_roles/job-roles.html", {"user": request.user})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admins').exists() or u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def add_job_role(request):
    return render(request, "job_roles/add_job_role.html")
