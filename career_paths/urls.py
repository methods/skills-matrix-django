from django.urls import path

from . import views

urlpatterns = [
    path('/browse', views.browse_career_paths, name='browse career path'),
]