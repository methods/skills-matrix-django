from django.shortcuts import render, redirect
from common.custom_class_view import CustomView
from common.user_group_check_mixins import AdminUserMixin
from .models import Skill
from .forms import SkillForm


class ViewSkillsView(AdminUserMixin, CustomView):
    def get(self, request):
        skills = Skill.objects.order_by('name')
        return render(request, 'skills/view_skills.html', {'skills': skills})

    def delete(self, request):
        Skill.objects.get(pk=request.POST['delete']).delete()
        skills = Skill.objects.order_by('name')
        return render(request, 'skills/view_skills.html', {'skills': skills})


class AddSkillView(AdminUserMixin, CustomView):
    def get(self, request):
        form = SkillForm()
        return render(request, 'skills/create_edit_skill.html', {'form': form})

    def post(self, request):
        form = SkillForm(request.POST)
        if form.is_valid():
            form.process()
        return redirect('view-skills')


class EditSkillView(AdminUserMixin, CustomView):
    def get(self, request, pk):
        skill = Skill.objects.get(pk=pk)
        form = SkillForm(initial={'skill_name': skill.name, 'skill_description': skill.description, 'team': skill.team})
        return render(request, 'skills/create_edit_skill.html', {'form': form, 'edit': True})

    def post(self, request, pk):
        form = SkillForm(request.POST)
        if form.is_valid():
            form.process_edit(pk)
        return redirect('view-skills')
