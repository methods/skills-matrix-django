from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


class AdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        group = self.request.user.groups
        if group.filter(name='Super admins').exists() or group.filter(name='Admins').exists():
            return True
        else:
            if self.request.user.is_authenticated:
                return False

    def handle_no_permission(self):
        return redirect(reverse('not authorised'))


class SuperAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        group = self.request.user.groups
        if group.filter(name='Super admins').exists():
            return True
        else:
            if self.request.user.is_authenticated:
                return False

    def handle_no_permission(self):
        return redirect(reverse('not authorised'))
