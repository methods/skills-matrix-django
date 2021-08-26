from . import views
from django.urls import path


urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin-dashboard')
]
