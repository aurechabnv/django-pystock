import pytest
from django.test import Client
from django.urls import reverse


def test_users_view_unauthenticated_access(client: Client):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("management:user-list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_users_view_unauthorized_access(client: Client, user1):
    """
    Test that a non-staff member cannot access the view
    """
    client.force_login(user1)
    response = client.get(reverse("management:user-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_users_view_authenticated_access(client: Client, user2, user1):
    """
    Test that a staff member can access the view
    """
    client.force_login(user2)
    response = client.get(reverse("management:user-list"))
    assert response.context.get("object_list").count() == 2
    assert response.status_code == 200
