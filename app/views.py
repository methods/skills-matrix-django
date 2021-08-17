from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from job_roles.models import Competency, Job
from skills.models import UserCompetencies
from app.forms import UserSkillLevelForm


@login_required
def dashboard(request):
    job_role_title = Job.objects.get(job_title=request.user.job_role)
    competency_list = Competency.objects.filter(job_role_title=job_role_title.id)
    individual_competency_list = UserCompetencies.objects.filter(user=request.user.id)
    return render(request, "app/dashboard.html", {"competency_list": competency_list,
                                                  "individual_competency_list": individual_competency_list})


@login_required
def edit_skills(request):
    job_role_title = Job.objects.get(job_title=request.user.job_role)
    competency_list = Competency.objects.filter(job_role_title=job_role_title.id)
    # form = UserSkillLevelForm(initial={'user_skill_level': competency.job_role_skill_level.name})
    if request.method == 'POST':
        form = UserSkillLevelForm(request.POST)
        if form.is_valid():
            return redirect(dashboard)
    return render(request, "app/edit_skills.html", {"competency_list": competency_list, "form": form})


@login_required
def browse_profiles(request):
    return render(request, 'app/browse_profiles.html')
