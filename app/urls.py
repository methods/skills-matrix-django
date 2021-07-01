from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='index'),
    path('edit-skills', views.edit_skills, name='edit skills'),
]
