from django.urls import path

from . import views

urlpatterns = [
    path('skills', views.ViewSkills.as_view(), name='view-skills'),
]
