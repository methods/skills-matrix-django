from django.urls import path
from . import views

urlpatterns = [
    path('', views.ViewSkillLevels.as_view(), name='view-skill-levels'),
    path('add-a-skill-level/', views.AddSkillLevel.as_view(), name='add-a-skill-level'),
    path('edit-skill-level/<int:pk>/', views.EditSkillLevel.as_view(), name='edit-a-skill-level')
    ]
