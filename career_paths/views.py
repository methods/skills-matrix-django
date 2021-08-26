from django.shortcuts import render
from common.custom_class_view import CustomView
from common.user_group_check_mixins import CustomLoginRequiredMixin


class BrowseCareerPaths(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        return render(request, 'career_paths/browse_career_paths.html')

