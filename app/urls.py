from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('edit-skills/', views.EditSkills.as_view(), name='edit-skills'),
    path('browse-profiles/', views.BrowseProfiles.as_view(), name='browse-profiles'),
]
