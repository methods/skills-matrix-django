from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Super admins').exists(),
                  login_url='/error/not-authorised')
def view_skill_levels(request):
    return render(request, 'super_admin/view_skill_levels.html')
