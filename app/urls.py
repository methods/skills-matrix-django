from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-skill/', views.non_admin_add_skill, name='non-admin-create-skill'),
    path('edit-skills/', views.edit_skills, name='edit-skills'),
    path('browse-profiles/', views.browse_profiles, name='browse-profiles'),
]
