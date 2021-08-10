from django.urls import path

from . import views

urlpatterns = [
    path('', views.ViewSkillsView.as_view(), name='view-skills'),
    path('create-new-skill/', views.AddSkillsView.as_view(), name='admin-create-skill')
]
