import pytest
from django.test import Client
from django.urls import reverse


def test_locations_view_unauthenticated_access(client: Client):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("management:location-list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_users_view_unauthorized_access(client: Client, user1):
    """
    Test that a non-staff member cannot access the view
    """
    client.force_login(user1)
    response = client.get(reverse("management:location-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_locations_view_authenticated_access(client: Client, user2, location1, location2, location3):
    """
    Test that a staff member can access the view
    """
    client.force_login(user2)
    response = client.get(reverse("management:location-list"))
    assert response.context.get("object_list").count() == 3
    assert response.status_code == 200


@pytest.mark.django_db
def test_locations_view_query_filter(client: Client, user2, location1, location2, location3):
    """
    Test that the results can be filtered based on user search
    """
    client.force_login(user2)
    response = client.get(reverse("management:location-list"), {"q": "GPCP"})
    assert response.context.get("object_list").count() == 1
    assert "filters" in response.context
    assert "q" in response.context.get("filters")
    assert response.status_code == 200
