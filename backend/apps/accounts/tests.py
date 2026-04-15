import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from .models import User

@pytest.mark.django_db
class TestAccounts:

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            full_name='Test User',
            password='password123'
        )
        assert user.email == "testuser@example.com"
        assert isinstance(user.id, uuid.UUID)
        assert user.is_active is True

    def test_registration_api(self, client):
        url = reverse('register')
        data = {
            "email" : "newuser@example.com",
            "username" : "newuser",
            "full_name" : "New User",
            "password" : "newpassword123"
        }
        response = client.post(url, data, content_type = "application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_user_login(self, client):
        user = User.objects.create_user(
            email = "loginuser@example.com",
            username = "loginuser",
            password = "loginpassword123"
        )

        url = reverse("token_obtain_pair")
        data = {"email" : "loginuser@example.com", "password" : "loginpassword123"}

        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
