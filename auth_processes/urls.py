from django.urls import path
from .views import LoginView
from . import views


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/unauthorised', LoginView.as_view(extra_context={'unauthorised': True}), name='login-unauthorised'),
    path('logout/', views.logout, name='logout')
]
