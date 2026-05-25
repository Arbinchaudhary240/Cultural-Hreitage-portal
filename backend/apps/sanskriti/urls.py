from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EthnicityProfileViewSet

router = DefaultRouter()
router.register(r'profiles', EthnicityProfileViewSet, basename='ethnicity-profile')

urlpatterns = [
    path('', include(router.urls)),
]