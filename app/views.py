from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def dashboard(request):
    db = get_user_model()
    all_users = db.objects.all()
    context = {"users": all_users}
    return render(request, "app/dashboard.html", context)


def edit_skills(request):
    return render(request, "app/edit_skills.html")


def job_roles(request):
    if request.user.is_staff:
        return render(request, "app/job-roles.html", {"admin": True})
    return render(request, "app/job-roles.html")


@user_passes_test(lambda u: u.is_staff, login_url='/error/not-authorised')
def add_job_role(request):
    return render(request, "app/add_job_role.html")
