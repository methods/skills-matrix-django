from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-skill/', views.non_admin_add_skill, name='non-admin-add-skill'),
    path('create-skill/', views.user_create_skill, name='user-create-skill'),
    path('browse-profiles/', views.browse_profiles, name='browse-profiles'),
]
