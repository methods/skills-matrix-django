from . import views
from django.urls import path


urlpatterns = [
    path('', views.admin_dashboard_view, name='admin-dashboard')
]
