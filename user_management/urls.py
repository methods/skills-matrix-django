from django.urls import path

from . import views

urlpatterns = [
    path('signup/name/', views.AddName.as_view(), name='add-name'),
    path('signup/email/', views.AddEmail.as_view(), name='add-email'),
    path('signup/job/', views.AddJob.as_view(), name='add-job'),
    path('signup/create-password/', views.CreatePassword.as_view(), name='create-password'),
    path('signup/summary/', views.Summary.as_view(), name='summary'),
    path('signup/edit-name/', views.EditNameSignup.as_view(), name='edit-name-signup'),
    path('signup/edit-email-address/', views.EditEmailAddressSignup.as_view(), name='edit-email-address-signup'),
    path('signup/edit-job-information/', views.EditJobInformationSignup.as_view(), name='edit-job-information-signup'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/edit-name/', views.EditName.as_view(), name='edit-name'),
    path('profile/edit-email-address/', views.edit_email, name='edit-email-address'),
    path('profile/edit-job-information/', views.edit_job_information, name='edit-job-information'),
]
