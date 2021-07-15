from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import SkillLevel
from .forms import SkillLevelForm


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def view_skill_levels(request):
    if request.POST:
        if 'edit' in request.POST.keys():
            print('edit')
        if 'delete' in request.POST.keys():
            print(request.POST)
            SkillLevel.objects.filter(name=request.POST['delete']).delete()
    skill_levels = SkillLevel.objects.all()
    return render(request, 'super_admin/view_skill_levels.html', {'skill_levels': skill_levels})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def add_skill_level(request):
    if request.POST:
        form = SkillLevelForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            description = request.POST['description']
            SkillLevel.objects.create(name=name, description=description)
            return redirect(view_skill_levels)
    form = SkillLevelForm()
    return render(request, 'super_admin/add_skill_level.html', {'form': form})
