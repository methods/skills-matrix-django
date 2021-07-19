from django.urls import path

from . import views

urlpatterns = [
    path('signup/name/', views.add_name, name='add-name'),
    path('signup/email/', views.add_email, name='add-email'),
    path('signup/job/', views.add_job, name='add-job'),
    path('signup/create-password/', views.create_password, name='create-password'),
    path('signup/summary/', views.summary, name='summary'),
    path('signup/edit-name/', views.edit_name_signup, name='edit-name-signup'),
    path('signup/edit-email-address/', views.edit_email_address_signup, name='edit-email-address-signup'),
    path('signup/edit-job-information/', views.edit_job_information_signup, name='edit-job-information-signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit-name/', views.edit_name, name='edit-name'),
    path('profile/edit-email-address/', views.edit_email, name='edit-email-address'),
    path('profile/edit-job-information/', views.edit_job_information, name='edit-job-information'),
]
