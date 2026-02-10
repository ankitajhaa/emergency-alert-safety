"""
URL mappings for alert APIs.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from alerts import views

router = DefaultRouter()
router.register('', views.AlertViewSet, basename='alerts')

app_name = 'alerts'

urlpatterns = [
    path('', include(router.urls)),
]