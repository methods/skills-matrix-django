from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('edit-skills', views.edit_skills, name='edit skills'),
    path('job-roles', views.job_roles, name='job roles'),
    path('add-a-job-role', views.add_job_role, name='add a job role')
]
