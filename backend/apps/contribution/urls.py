from django.urls import path
from .views import ContributionCreateView

urlpatterns = [
    path("", ContributionCreateView.as_view(), name="contribution")
]
