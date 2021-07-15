from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import SkillLevel


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
