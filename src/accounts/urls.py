from django.urls import path
from .views import RegisterView,LoginView,DashboardView,health
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='for refresh token'),
    path('dashboard/',DashboardView.as_view(),name='for refresh token'),
    path("health/", health),
]
