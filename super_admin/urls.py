from django.urls import path
from . import views

urlpatterns = [
    path('/view-skill-levels', views.view_skill_levels, name='view skill levels'),
    ]
