from django.urls import path

from . import views

urlpatterns = [
    path('name', views.add_name, name='add name')
]
