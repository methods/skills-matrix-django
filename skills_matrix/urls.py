from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('user/', include('user_management.urls')),
    path('', include('app.urls')),
    path('admin', admin.site.urls),
    path('error/', include('error.urls')),
    path('job-roles/', include('job_roles.urls')),
    path('auth/', include('auth_processes.urls')),
    path('career-paths/', include('career_paths.urls')),
    path('super-admin/', include('super_admin.urls')),
    path('skills/', include('skills.urls')),
]
