import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from apps.sanskriti.models import EthnicityProfile

User = get_user_model()

@pytest.fixture
def test_user():
    """Creates a regular verified user for authenticated API requests."""
    return User.objects.create_user(username="sanskriti_editor", password="securepassword123")

@pytest.fixture
def api_client(test_user):
    """Provides an API client that is pre-authenticated with our test user."""
    client = APIClient()
    client.force_authenticate(user=test_user) # This clears your 401 Unauthorized barrier!
    return client
@pytest.fixture
def identity_tree():
    """Builds a multi-tier cultural tree model profile."""
    # 1. Tier 1 Root Node
    religion = EthnicityProfile.objects.create(
        name="Buddhism",
        node_type="religion"
    )
    # 2. Tier 2 Child Node
    caste = EthnicityProfile.objects.create(
        name="Newar",
        node_type="caste",
        parent=religion
    )
    # 3. Tier 3 Sub-Child Node
    subcaste = EthnicityProfile.objects.create(
        name="Shakya",
        node_type="subcaste",
        parent=caste,
        historical_background="Historically associated with traditional artisans and metallurgy."
    )
    
    return {
        "religion": religion,
        "caste": caste,
        "subcaste": subcaste,
        "list_url": reverse('ethnicity-profile-list')
    }

# Tests

@pytest.mark.django_db
def test_create_and_slugify_nodes(identity_tree):
    """Ensure that slugs generate automatically and hierarchy parents map correctly."""
    node = identity_tree["subcaste"]
    assert node.slug == "shakya"
    assert node.parent.name == "Newar"
    assert node.parent.parent.name == "Buddhism"


@pytest.mark.django_db
def test_get_profiles_list(api_client, identity_tree):
    """Verify that the API returns all created profiles correctly."""
    response = api_client.get(identity_tree["list_url"])
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3  # All 3 nodes should list globally


@pytest.mark.django_db
def test_nested_serialization_tree(api_client, identity_tree):
    """Ensure that querying a parent endpoint nests its downstream structural children."""
    # Query details for the parent 'Newar' caste node directly via its slug
    detail_url = reverse('ethnicity-profile-detail', kwargs={'slug': 'newar'})
    response = api_client.get(detail_url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Newar"
    # Ensure 'Shakya' shows up nested directly inside the children array
    assert len(response.data['children']) == 1
    assert response.data['children'][0]['name'] == "Shakya"


@pytest.mark.django_db
def test_node_type_filtering(api_client, identity_tree):
    """Verify the API filters data cleanly by its position node type."""
    list_url = identity_tree["list_url"]
    
    # Filter for only religions
    response = api_client.get(f"{list_url}?node_type=religion")
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Buddhism"