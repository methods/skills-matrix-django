from django.urls import path

from . import views

urlpatterns = [
    path('', views.ViewSkillsView.as_view(), name='view-skills'),
    path('create-new-skill/', views.AddSkillView.as_view(), name='admin-create-skill'),
    path('edit-skill/<int:pk>/', views.EditSkillView.as_view(), name='admin-edit-skill'),
]
