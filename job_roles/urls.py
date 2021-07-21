from . import views
from django.urls import path


urlpatterns = [
    path('', views.job_roles, name='job-roles'),
    path('create-new-job/', views.add_job_role, name='add-a-job-role')
]
