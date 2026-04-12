from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'password', 'phone', 'country', 'city', 'profile', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'id ': {'read_only': True},
            'date_joined': {'read_only': True},
            }
        
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user