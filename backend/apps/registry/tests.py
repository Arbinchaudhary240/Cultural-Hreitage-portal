import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Category, HeritageItem
# from django.contrib.auth import get_user_model
from apps.contribution.models import Contribution
from apps.accounts.models import User

@pytest.mark.django_db
class TestContributions:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def setup_data(self, api_client):
        user = User.objects.create_user(email="testuser@gmail.com",username="testuser", password="testuser")

        category = Category.objects.create(
            name = "Tangible Heritage",
            slug = "tangible-heritage",
            description = "physical artifacts"
        )
        contribution = Contribution.objects.create(
            title="Patan Durbar Square",
            description="An ancient palace complex in Lalitpur.",
            contributer=user,
            status="approved"
        )
        heritage_item = HeritageItem.objects.create(
            official_name="Patan Durbar Square Official",
            category=category,
            contribution=contribution,
            description="heritage of nepal"
        )
        api_client.force_authenticate(user=user)
        return {
            "item": heritage_item,
            "list_url": reverse("heritage-item-list"),
            "category_url": reverse('category-list')
        }

    # Tests
    @pytest.mark.django_db
    def test_get_heritage_item_list(self,api_client, setup_data):
        response = api_client.get(setup_data["list_url"])
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['official_name'] == "Patan Durbar Square Official"
    @pytest.mark.django_db
    def test_serializer_maps_contribution_description(self, api_client, setup_data):
        response = api_client.get(setup_data["list_url"])
        assert response.data[0]['contributor_description'] == "An ancient palace complex in Lalitpur."
    @pytest.mark.django_db
    def test_search_filter_works(self, api_client, setup_data):
        list_url = setup_data['list_url']
        response = api_client.get(f"{list_url}?search=Patan")
        assert len(response.data) == 1
        response = api_client.get(f"{list_url}?search=Bhaktapur")
        assert len(response.data)== 0
    @pytest.mark.django_db
    def test_category_filter_works(self, api_client, setup_data):
        list_url = setup_data["list_url"]
        response = api_client.get(f"{list_url}?category__slug=tangible-heritage")
        assert len(response.data) == 1
        response = api_client.get(f"{list_url}?category__slug=food")
        assert len(response.data) == 0