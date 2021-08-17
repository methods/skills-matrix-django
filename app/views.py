from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from job_roles.models import Competency, Job
from skills.models import UserCompetencies


@login_required
def dashboard(request):
    job_role_title = Job.objects.get(job_title=request.user.job_role)
    competency_list = Competency.objects.filter(job_role_title=job_role_title.id)
    individual_competency_list = UserCompetencies.objects.filter(user=request.user.id)
    return render(request, "app/dashboard.html", {"competency_list": competency_list,
                                                  "individual_competency_list": individual_competency_list})


@login_required
def edit_skills(request):
    return render(request, "app/edit_skills.html")


@login_required
def browse_profiles(request):
    return render(request, 'app/browse_profiles.html')
