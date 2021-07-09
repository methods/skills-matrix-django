from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'auth_processes/login.html'
    redirect_authenticated_user = True


@login_required
def logout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('/auth/login')
    return render(request, 'auth_processes/logout.html')
