from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_roles, name='job roles'),
    path('/add-job-role-title', views.add_job_role, name='add_job_title'),
    path('/add-job-role-skills', views.add_job_role_skills, name='add_job_skills'),
    path('/review-job-role', views.review_job_role, name='review_job_role_details'),
    path('/<str:job>', views.dynamic_job_role_lookup_view, name='job role view'),
    path('/update/<str:job_title>', views.update_job_role_detail_view, name='update job role view')
]
