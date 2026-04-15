from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User, Contribution
from .serializers import UserSerializer, RegisterSerializer, ContributionSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Anyone can register
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ContributionCreateView(generics.CreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Contribution.objects.filter(contributer=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(contributer=self.request.user)