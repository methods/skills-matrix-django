from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('signup/', include('signup.urls')),
    path('', include('app.urls')),
    path('admin', admin.site.urls),
    path('error/', include('error.urls')),
    path('job-roles', include('job_roles.urls')),
    path('auth', include('auth_processes.urls')),
    path('profile', include('user_profile.urls'))
]
