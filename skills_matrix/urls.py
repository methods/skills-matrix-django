from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('user/', include('user_management.urls')),
    path('', include('app.urls')),
    path('admin-dashboard/', include('admin_user.urls')),
    path('error/', include('error.urls')),
    path('job-roles/', include('job_roles.urls')),
    path('auth/', include('auth_processes.urls')),
    path('career-paths/', include('career_paths.urls')),
    path('skill-levels/', include('super_admin.urls_skill_level')),
    path('skills/', include('skills.urls')),
    path('admin', admin.site.urls),
]
