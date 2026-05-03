import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User
from .models import Contribution

@pytest.mark.django_db
class TestContributions:

    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    def test_contribution_creation(self):
        user = User.objects.create_user(email="testuser@gmail.com",username="testuser", password="testuser")

        contribution = Contribution.objects.create(
            contributer = user,
            title= "jitiya",
            description = "festival celebrated by women"
        )

        assert isinstance(contribution.id, uuid.UUID)
        assert Contribution.objects.filter(title="jitiya").exists()

    
    def test_user_contribution(self, api_client):
        user = User.objects.create_user(
            email= "contributer@example.com",
            username= "happy",
            password= "happy123"
        )

        login_url = reverse("token_obtain_pair")
        login_data = {"email":"contributer@example.com", "password":"happy123"}

        response = api_client.post(login_url, login_data)
        assert response.status_code == status.HTTP_200_OK
        token = response.data["access"]

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("contribution")
        data = {
            "title": "siruwa",
            "description": "SIRUWA is a festival celebrated in  new year"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Contribution.objects.filter(title="siruwa").exists()