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
        Skill.objects.filter(pk=request.POST['delete']).delete()
        skills = Skill.objects.order_by('name')
        return render(request, 'skills/view_skills.html', {'skills': skills})


class AddSkillsView(AdminUserMixin, CustomView):
    def get(self, request):
        form = SkillForm()
        return render(request, 'skills/create_skill.html', {'form': form})
