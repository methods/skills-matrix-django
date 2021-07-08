from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


def job_roles(request):
    if request.user.is_staff:
        return render(request, "job_roles/job-roles.html", {"admin": True})
    return render(request, "job_roles/job-roles.html")


@user_passes_test(lambda u: u.is_staff, login_url='/error/not-authorised')
def add_job_role(request):
    return render(request, "job_roles/add_job_role.html")
