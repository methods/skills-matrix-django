from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from job_roles.models import Competency, Job
from skills.models import UserCompetencies
from app.forms import UserSkillLevelForm
from app.view_utils import prepare_competency_update
from super_admin.models import SkillLevel


@login_required
def dashboard(request):
    job_role_title = Job.objects.get(job_title=request.user.job_role)
    competency_list = Competency.objects.filter(job_role_title=job_role_title.id).order_by('id')
    individual_competency_list = UserCompetencies.objects.filter(user=request.user.id).order_by('id')
    if 'update-competency' in request.POST.keys():
        template_variables = prepare_competency_update(request.POST['update-competency'])
        return render(request, "app/dashboard.html", {'form': template_variables['form'], "competency_list": competency_list,'update_competency_id': template_variables['update_competency_id']})
    if 'save-skill-level' in request.POST.keys():
        form = UserSkillLevelForm(request.POST)
        if form.is_valid():
            Competency.objects.filter(id=request.POST['save-skill-level']).update(job_role_skill_level=SkillLevel.objects.get(name=form.cleaned_data['user_skill_level']).id)
    return render(request, "app/dashboard.html", {"competency_list": competency_list,
                                                  "individual_competency_list": individual_competency_list})


@login_required
def edit_skills(request, pk):
    job_role_title = Job.objects.get(job_title=request.user.job_role)
    competency_list = Competency.objects.filter(job_role_title=job_role_title.id)
    competency_object = Competency.objects.get(id=pk)
    form = UserSkillLevelForm(initial={'user_skill_level': competency_object.job_role_skill_level.name})
    if request.method == 'POST':
        form = UserSkillLevelForm(request.POST)
        if form.is_valid():
            return redirect(dashboard)
    return render(request, "app/edit_skills.html", {"competency_list": competency_list, "form": form})


@login_required
def browse_profiles(request):
    return render(request, 'app/browse_profiles.html')
