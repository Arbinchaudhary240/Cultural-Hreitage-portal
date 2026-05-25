from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EthnicityProfile
from .serializers import EthnicityProfileSerializer

class EthnicityProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that displays cultural demographics.
    Allows filtering by type (e.g., /?node_type=caste) or finding sub-nodes.
    """
    serializer_class = EthnicityProfileSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['node_type', 'parent__slug']
    search_fields = ['name', 'historical_background']

    def get_queryset(self):
        # Prefetch children to prevent N+1 database querying issues at high traffic
        return EthnicityProfile.objects.select_related('parent').prefetch_related('children').all()