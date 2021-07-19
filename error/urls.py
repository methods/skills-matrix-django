from django.urls import path
from . import views


urlpatterns = [
    path('not-authorised/', views.not_authorised, name='not authorised')
]
