from django.urls import path
from . import views

urlpatterns = [
    path('view-skill-levels/', views.view_skill_levels, name='view-skill-levels'),
    path('add-a-skill-level/', views.add_skill_level, name='add-a-skill-level'),
    path('edit-skill-level/<int:pk>/', views.edit_skill_level, name='edit-a-skill-level')
    ]