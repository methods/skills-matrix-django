from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from job_roles.models import Competency, Job
from skills.models import UserCompetencies, Skill
from app.forms import UserSkillLevelForm, UserSkillDefinitionForm, UserSkillForm,CreateUserSkillForm
from app.view_utils import prepare_competency_update,retrieve_user_skills, prepare_non_job_related_competency_update,populate_existing_user_competencies
from super_admin.models import SkillLevel
from user_management.models import NewUser


@login_required
def dashboard(request):
    job_role_competency_list = Competency.objects.filter(job_role_title=Job.objects.get(job_title=request.user.job_role).id).order_by('id')
    individual_competency_list = UserCompetencies.objects.filter(job_role_related=False, user=request.user.id).order_by('id')
    user_skills = []
    existing_skill_list = retrieve_user_skills(user_skills, request)
    for competency in job_role_competency_list:
        if UserCompetencies.objects.filter(skill=competency.job_role_skill.id,user=request.user.id,job_role_related=False).exists():
            UserCompetencies.objects.filter(skill=competency.job_role_skill.id,user=request.user.id,job_role_related=False).update(job_role_related=True)
    individual_job_related_competency_list = UserCompetencies.objects.filter(job_role_related=True, user=request.user.id).order_by('id')
    for individual_job_related_competency in individual_job_related_competency_list:
        if not Competency.objects.filter(job_role_title=Job.objects.get(job_title=request.user.job_role), job_role_skill=individual_job_related_competency.skill).exists():
            UserCompetencies.objects.filter(skill=individual_job_related_competency.skill,user=request.user.id).update(job_role_related=False)
    if 'update-competency' in request.POST.keys():
        template_variables = prepare_competency_update(request.POST['update-competency'], request)
        return render(request, "app/dashboard.html", {'form': template_variables['form'],
                                                      'update_existing_skill_id': template_variables['update_existing_skill_id'],
                                                      "job_role_competency_list": job_role_competency_list,
                                                      "all_user_competencies": UserCompetencies.objects.filter(user=request.user.id).order_by('id'),
                                                      "user_skills": existing_skill_list})
    if 'save' in request.POST.keys():
        form = UserSkillLevelForm(request.POST)
        if form.is_valid():
            if not UserCompetencies.objects.filter(skill=Skill.objects.get(id=request.POST['save']),user=request.user.id).exists():
                job_competency = Competency.objects.get(job_role_skill=Skill.objects.get(id=request.POST['save']), job_role_title=Job.objects.get(job_title=request.user.job_role).id)
                UserCompetencies.objects.create(user=NewUser.objects.get(id=request.user.id),
                                                skill=Skill.objects.get(id=job_competency.job_role_skill.id),
                                                skill_level=SkillLevel.objects.get(name=form.cleaned_data['user_skill_level']))
                user_skills = []
                existing_skill_list = retrieve_user_skills(user_skills, request)
            elif UserCompetencies.objects.filter(skill=Skill.objects.get(id=request.POST['save']),job_role_related=True,user=request.user.id).exists():
                UserCompetencies.objects.filter(user=request.user.id, job_role_related=True, skill=Skill.objects.get(id=request.POST['save'])).update(skill_level=SkillLevel.objects.get(name=form.cleaned_data['user_skill_level']).id)
    if 'delete' in request.POST.keys():
        if UserCompetencies.objects.filter(id=request.POST['delete'], user=request.user.id, job_role_related=False).exists():
            UserCompetencies.objects.get(id=request.POST['delete'], user=request.user.id, job_role_related=False).delete()
    if "edit-user-skill" in request.POST.keys():
        if UserCompetencies.objects.filter(id=request.POST['edit-user-skill'], user=request.user.id, job_role_related=False).exists():
            user_template_variables=prepare_non_job_related_competency_update(request.POST['edit-user-skill'], request)
        return render(request, "app/dashboard.html", {'form_user_skill': user_template_variables['form_user_skill'],
                                                      'form_user_skill_level': user_template_variables['form_user_skill_level'],
                                                      'existing_user_competency_id': user_template_variables['existing_user_competency_id'],
                                                      "job_role_competency_list": job_role_competency_list,
                                                      "individual_competency_list": UserCompetencies.objects.filter(job_role_related=False, user=request.user.id).order_by('id'),
                                                      "all_user_competencies": UserCompetencies.objects.filter(user=request.user.id).order_by('id'),
                                                      "user_skills": existing_skill_list})
    if 'save_existing_user_competency' in request.POST.keys():
        user_competency_object = UserCompetencies.objects.get(id=request.POST['save_existing_user_competency'], user=request.user.id, job_role_related=False)
        if not user_competency_object.skill.team:
            form_user_skill = UserSkillDefinitionForm(request.POST)
            form_user_skill_level = UserSkillLevelForm(request.POST)
            if form_user_skill.is_valid() and form_user_skill_level.is_valid():
                user_competency_to_update = UserCompetencies.objects.get(id=request.POST['save_existing_user_competency'], user=request.user.id, job_role_related=False)
                Skill.objects.filter(id=user_competency_to_update.skill.id).update(name=form_user_skill.cleaned_data['user_skill_definition'])
                UserCompetencies.objects.filter(user=request.user.id, job_role_related=False, id=request.POST['save_existing_user_competency']).update(skill_level=SkillLevel.objects.get(name=form_user_skill_level.cleaned_data['user_skill_level']).id)
        else:
            form_user_skill_level = UserSkillLevelForm(request.POST)
            if form_user_skill_level.is_valid():
                UserCompetencies.objects.filter(user=request.user.id, job_role_related=False, id=request.POST['save_existing_user_competency']).update(skill_level=SkillLevel.objects.get(name=form_user_skill_level.cleaned_data['user_skill_level']).id)

    return render(request, "app/dashboard.html", {"job_role_competency_list": Competency.objects.filter(job_role_title=Job.objects.get(job_title=request.user.job_role).id).order_by('id'),
                                                  "individual_competency_list": individual_competency_list,
                                                  "all_user_competencies":UserCompetencies.objects.filter(user=request.user.id).order_by('id'),
                                                  "user_skills":existing_skill_list})

@login_required
def non_admin_add_skill(request):
    if request.POST:
        disabled_choices = populate_existing_user_competencies(request)
        form_user_skill_level = UserSkillLevelForm(request.POST)
        form_user_skill = UserSkillForm(request.POST, disabled_choices=disabled_choices)
        if form_user_skill_level.is_valid() and form_user_skill.is_valid():
            UserCompetencies.objects.create(user=NewUser.objects.get(id=request.user.id),
                                            skill=Skill.objects.get(name=form_user_skill.cleaned_data['user_skill']),
                                            skill_level=SkillLevel.objects.get(name=form_user_skill_level.cleaned_data['user_skill_level']),
                                            job_role_related=False)
            return redirect('/dashboard/#additional-skills')
    else:
        disabled_choices = populate_existing_user_competencies(request)
        form_user_skill_level = UserSkillLevelForm()
        form_user_skill = UserSkillForm(disabled_choices=disabled_choices)
    return render(request, "app/add_skill.html", {'form_user_skill_level': form_user_skill_level, "form_user_skill": form_user_skill})


@login_required
def user_create_skill(request):
    if request.POST:
        form = CreateUserSkillForm(request.POST)
        if form.is_valid():
            Skill.objects.create(name=form.cleaned_data["user_skill_definition"], description=form.cleaned_data['skill_description'], team=None)
            return redirect(non_admin_add_skill)
    else:
        form = CreateUserSkillForm()
    return render(request, 'skills/create_edit_skill.html', {"form": form})


@login_required
def browse_profiles(request):
    return render(request, 'app/browse_profiles.html')
