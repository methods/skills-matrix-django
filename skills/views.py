from django.shortcuts import render, redirect
from django.views import View
from common.user_group_check_mixins import AdminUserMixin
from .models import Skill


class ViewSkills(AdminUserMixin, View):
    def get(self, request):
        skills = Skill.objects.all()
        return render(request, 'skills/view_skills.html', {'skills': skills})
