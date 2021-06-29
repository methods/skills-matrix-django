from django.urls import path

from . import views

urlpatterns = [
    path('name', views.add_name, name='add name'),
    path('email/', views.add_email, name='add email'),
    path('job/', views.add_job, name='add job'),
    path('create-password/', views.create_password, name='create password'),
    path('summary/', views.summary, name='summary')
]
