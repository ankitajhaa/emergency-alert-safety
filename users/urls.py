"""
URL mappings for the user API.
"""
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]