from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect, render
from common.custom_class_view import CustomView
from common.user_group_check_mixins import CustomLoginRequiredMixin


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'auth_processes/login.html'
    redirect_authenticated_user = True


class Logout(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        return render(request, 'auth_processes/logout.html')

    def post(self, request):
        django_logout(request)
        return redirect('/auth/login')

