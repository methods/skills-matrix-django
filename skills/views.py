from django.shortcuts import render, redirect
from django.views import View
from common.user_group_check_mixins import AdminUserMixin


class ViewSkills(AdminUserMixin, View):
    def get(self, request):
        return render(request, 'skills/view_skills.html')
