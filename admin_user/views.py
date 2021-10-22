from django.shortcuts import render
from common.custom_class_view import CustomView
from common.user_group_check_mixins import CustomLoginRequiredMixin, AdminUserMixin


class AdminDashboardView(CustomLoginRequiredMixin, AdminUserMixin, CustomView):
    def get(self, request):
        return render(request, 'admin_user/admin_dashboard.html')
