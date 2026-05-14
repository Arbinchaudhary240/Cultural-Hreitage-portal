from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, HeritageItem
from .seriakizers import CategorySerializer, HeritageItemSerializer

class CategoryVeiwSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

class HeritageItemVeiwSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HeritageItemSerializer

    filter_backends = [
        DjangoFilterBackend,   # For exact matches (Category)
        filters.SearchFilter,  # For text search (Name/Description)
        filters.OrderingFilter # To sort by newest/oldest
    ]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug'] 
    search_fields = ['official_name', 'contribution__description']

    def get_queryset(self):
        return HeritageItem.objects.select_related('category', 'contribution').all()
