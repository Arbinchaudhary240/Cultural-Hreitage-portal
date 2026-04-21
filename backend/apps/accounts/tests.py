import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from .models import User, Contribution
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestAccounts:

    @pytest.fixture
    def api_client(self):
        return APIClient()

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

    def test_registration_api(self, api_client):
        url = reverse('register')
        data = {
            "email" : "newuser@example.com",
            "username" : "newuser",
            "full_name" : "New User",
            "password" : "newpassword123"
        }
        response = api_client.post(url, data, content_type = "application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_user_login(self, api_client):
        user = User.objects.create_user(
            email = "loginuser@example.com",
            username = "loginuser",
            password = "loginpassword123"
        )

        url = reverse("token_obtain_pair")
        data = {"email" : "loginuser@example.com", "password" : "loginpassword123"}

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    
    def test_user_contribution(self, api_client):
        user = User.objects.create_user(
            email="contributer@example.com",
            username="Contributer",
            password="contributer123"
        )

        login_url = reverse("token_obtain_pair")
        login_data = {"email": "contributer@example.com", "password": "contributer123"}
        response = api_client.post(login_url, login_data)
        
        assert response.status_code == status.HTTP_200_OK
        token = response.data["access"]

        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse("contribute")
        contribution_data = {
            "title": "siruwa",
            "description": "this is celebreted in new year"
        }
        response = api_client.post(url, contribution_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Contribution.objects.filter(title="siruwa").exists()
    
    def test_double_user_creation_with_same_email(self, api_client):
        url = reverse('register')
        data_1 = {
            "email": "sameuser@example.com",
            "full_name": "sameuser",
            "username": "sameuser",
            "password": "user1_9898"
        }
        response1 = api_client.post(url, data_1, content_type = "application/json")
        assert response1.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="sameuser@example.com").exists()
        print(response1.data)

        data_2 = {
            "email": "sameuser@example.com",
            "full_name": "sameuser",
            "username": "sameuser",
            "password": "user2_9898" 
        }
        response2 = api_client.post(url, data_2, content_type = "application/json")
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        