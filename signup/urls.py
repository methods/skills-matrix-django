from django.urls import path

from . import views

urlpatterns = [
    path('name', views.add_name, name='add name'),
    path('email/', views.add_email, name='add email'),
    path('job/', views.add_job, name='add job'),
    path('create-password/', views.create_password, name='create password'),
    path('summary/', views.summary, name='summary'),
    path('edit-name/', views.edit_name, name='edit name'),
    path('edit-email-address/', views.edit_email_address, name='edit email address'),
    path('edit-job-information/', views.edit_job_information, name='edit job information')
]
