from rest_framework import serializers
from .models import User, Contribution

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone', 'country', 'city', 'profile', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user
    
class ContributionSerializer(serializers.ModelSerializer):
    contributer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contribution
        fields = ["id", "contributer", "title", "description", "image", "audio", "vedio", "added_at"]
        read_only_fields = ["id", "added_at"]
        