from django.urls import path
from .views import LoginView
from . import views


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout', views.logout, name='log out')
]
