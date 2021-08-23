from django.urls import path
from . import views


urlpatterns = [
    path('not-authorised/', views.Unauthorised.as_view(), name='not authorised'),
    path('forbidden/', views.Forbidden.as_view(), name='forbidden')
]
