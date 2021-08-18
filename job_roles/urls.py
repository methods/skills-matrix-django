from . import views
from django.urls import path


urlpatterns = [
    path('', views.JobRoles.as_view(), name='job-roles'),
    path('add-job-role-title/', views.AddJobRole.as_view(), name='add-job-title'),
    path('add-job-role-skills/', views.AddJobRoleSkills.as_view(), name='add-job-skills'),
    path('review-job-role/', views.ReviewJobRole.as_view(), name='review-job-role-details'),
    path('<str:job>/', views.DynamicJobRoleLookup.as_view(), name='job-role-view'),
    path('update/<str:job_title>/', views.UpdateJobRoleDetail.as_view(), name='update-job-role-view'),
    path('update/<str:job_title>/add-a-skill/', views.add_a_skill, name='add-a-skill'),
    path('delete/<str:job_title>/', views.delete_job_role_title_view, name='delete-job-role-view')
]
