from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import SkillLevel
from .forms import SkillLevelForm
from common.custom_class_view import CustomView
from common.user_group_check_mixins import CustomLoginRequiredMixin, SuperAdminUserMixin


class ViewSkillLevels(CustomLoginRequiredMixin, SuperAdminUserMixin, CustomView):
    def get(self, request):
        skill_levels = SkillLevel.objects.all()
        return render(request, 'super_admin/view_skill_levels.html', {'skill_levels': skill_levels})

    def delete(self, request):
        SkillLevel.objects.filter(name=request.POST['delete']).delete()
        skill_levels = SkillLevel.objects.all()
        return render(request, 'super_admin/view_skill_levels.html', {'skill_levels': skill_levels})


class AddSkillLevel(CustomLoginRequiredMixin, SuperAdminUserMixin, CustomView):
    def get(self, request):
        form = SkillLevelForm()
        return render(request, 'super_admin/skill_level.html', {'form': form})

    def post(self, request):
        form = SkillLevelForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            SkillLevel.objects.create(name=name, description=description)
            return redirect('view-skill-levels')


class EditSkillLevel(CustomLoginRequiredMixin, SuperAdminUserMixin, CustomView):
    def set_form_initial_values(self, name, description):
        form = SkillLevelForm(initial={'name': name, 'description': description})
        return form

    def get(self, request, pk):
        skill_level = SkillLevel.objects.filter(pk=pk)
        form = self.set_form_initial_values(skill_level[0].name, skill_level[0].description)
        return render(request, 'super_admin/skill_level.html', {'form': form, 'edit': True})

    def post(self, request, pk):
        skill_level = SkillLevel.objects.filter(pk=pk)
        form = SkillLevelForm(request.POST)
        if form.is_valid():
            skill_level.update(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
            return redirect('view-skill-levels')
        form = self.set_form_initial_values(skill_level[0].name, skill_level[0].description)
        return render(request, 'super_admin/skill_level.html', {'form': form, 'edit': True})
