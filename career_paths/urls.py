from django.urls import path

from . import views

urlpatterns = [
    path('browse/', views.BrowseCareerPaths.as_view(), name='browse-career-paths'),
]