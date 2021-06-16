from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/edit-skills', views.edit_skills, name='edit skills')
]
