from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from job_roles.models import Competency, Job
from skills.models import UserCompetencies, Skill
from app.forms import UserSkillLevelForm
from app.view_utils import prepare_competency_update,retrieve_user_skills
from super_admin.models import SkillLevel
from user_management.models import NewUser


@login_required
def dashboard(request):
    job_role_competency_list = Competency.objects.filter(job_role_title=Job.objects.get(job_title=request.user.job_role).id).order_by('id')
    individual_competency_list = UserCompetencies.objects.filter(job_role_related=False, user=request.user.id).order_by('id')
    all_user_competency = UserCompetencies.objects.filter(user=request.user.id).order_by('id')
    user_skills = []
    existing_skill_list=retrieve_user_skills(all_user_competency,user_skills)
    # for competency in job_role_competency_list:
    #     if not UserCompetencies.objects.filter(skill=competency.job_role_skill.id,user=request.user.id).exists():
    #         UserCompetencies.objects.create(user=NewUser.objects.get(id=request.user.id),
    #                                         skill=Skill.objects.get(id=competency.job_role_skill.id),
    #                                         skill_level=SkillLevel.objects.get(name="Beginner"))
    #     elif UserCompetencies.objects.filter(skill=competency.job_role_skill.id,user=request.user.id,job_role_related=False).exists():
    #         UserCompetencies.objects.filter(skill=competency.job_role_skill.id,user=request.user.id,job_role_related=False).update(job_role_related=True)
    individual_job_related_competency_list = UserCompetencies.objects.filter(job_role_related=True, user=request.user.id).order_by('id')
    # for individual_job_related_competency in individual_job_related_competency_list:
    #     if not Competency.objects.filter(job_role_title=Job.objects.get(job_title=request.user.job_role), job_role_skill=individual_job_related_competency.skill).exists():
    #         UserCompetencies.objects.filter(skill=individual_job_related_competency.skill,user=request.user.id).update(job_role_related=False)
    if 'update-competency' in request.POST.keys():
        template_variables = prepare_competency_update(request.POST['update-competency'], request)
        return render(request, "app/dashboard.html", {'form': template_variables['form'],
                                                      'update_existing_skill_id': template_variables['update_existing_skill_id'],
                                                      "individual_job_related_competency_list": individual_job_related_competency_list,
                                                      "job_role_competency_list": job_role_competency_list,
                                                      "all_user_competency": all_user_competency,
                                                      "user_skills": existing_skill_list})
    if 'save-skill-level' in request.POST.keys():
        if not UserCompetencies.objects.filter(skill=request.POST['update-competency'],user=request.user.id).exists():
            form = UserSkillLevelForm(request.POST)
            if form.is_valid():
                UserCompetencies.objects.filter(user=request.user.id, id=request.POST['save-skill-level']).update(skill_level=SkillLevel.objects.get(name=form.cleaned_data['user_skill_level']).id)
    return render(request, "app/dashboard.html", {"job_role_competency_list": Competency.objects.filter(job_role_title=Job.objects.get(job_title=request.user.job_role).id).order_by('id'),
                                                  "individual_competency_list": individual_competency_list,
                                                  "individual_job_related_competency_list": UserCompetencies.objects.filter(job_role_related=True, user=request.user.id).order_by('id'), "job_role_competency_list": job_role_competency_list,
                                                  "all_user_competency":all_user_competency,
                                                  "user_skills":existing_skill_list})


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
