from django.shortcuts import render
from job_roles.models import Competency, Job
from skills.models import UserCompetencies
from common.custom_class_view import CustomView
from common.user_group_check_mixins import CustomLoginRequiredMixin


class Dashboard(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        job_role_title = Job.objects.get(job_title=request.user.job_role)
        competency_list = Competency.objects.filter(job_role_title=job_role_title.id)
        individual_competency_list = UserCompetencies.objects.filter(user=request.user.id)
        return render(request, "app/dashboard.html", {"competency_list": competency_list,
                                                      "individual_competency_list": individual_competency_list})


class EditSkills(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        return render(request, "app/edit_skills.html")


class BrowseProfiles(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        return render(request, 'app/browse_profiles.html')

