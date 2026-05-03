from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ContributionSerializer
from .models import Contribution
from django.shortcuts import render

# Create your views here.
class ContributionCreateView(generics.CreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Contribution.objects.filter(contributer=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(contributer=self.request.user)