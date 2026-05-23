from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, HeritageItem
from .serializers import CategorySerializer, HeritageItemSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

class HeritageItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HeritageItemSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug'] 
    search_fields = ['official_name', 'contribution__description']

    def get_queryset(self):
        return HeritageItem.objects.select_related('category', 'contribution').all()
