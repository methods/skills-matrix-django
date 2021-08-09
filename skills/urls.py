from django.urls import path

from . import views

urlpatterns = [
    path('', views.ViewSkills.as_view(), name='view-skills'),
]
