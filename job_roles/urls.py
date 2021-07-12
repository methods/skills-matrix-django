from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_roles, name='job roles'),
    path('/add-job-role-title', views.add_job_role, name='add_job_title'),
    path('/add-job-role-skills', views.add_job_role_skills, name='add_job_skills')
]
