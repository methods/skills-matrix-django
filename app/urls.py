from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='app/login.html', redirect_field_name='dashboard/',
                                          redirect_authenticated_user=True)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-skills', views.edit_skills, name='edit skills'),
]
