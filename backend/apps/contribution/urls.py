from django.urls import path
from .views import ContributionCreateView, ContributionUpdateView

app_name = 'contribution'

urlpatterns = [
    path("", ContributionCreateView.as_view(), name='contribute'),
    path("<uuid:pk>/", ContributionUpdateView.as_view(), name="detail"),
]
