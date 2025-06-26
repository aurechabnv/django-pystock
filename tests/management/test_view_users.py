import pytest
from django.test import Client
from django.urls import reverse


def test_user_list_view_unauthenticated_access(client: Client):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("management:user:list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_list_view_unauthorized_access(client: Client, user1):
    """
    Test that a non-staff member cannot access the view
    """
    client.force_login(user1)
    response = client.get(reverse("management:user:list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_list_view_unauthorized_staff_access(client: Client, user4):
    """
    Test that a staff member without permissions cannot access the view
    """
    client.force_login(user4)
    response = client.get(reverse("management:user:list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_list_view_authenticated_access(client: Client, user1, user2):
    """
    Test that a staff member can access the view
    """
    client.force_login(user2)
    response = client.get(reverse("management:user:list"))
    assert response.context.get("object_list").count() == 2
    assert response.status_code == 200


def test_user_add_view_unauthenticated_access(client: Client):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("management:user:add"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_add_view_unauthorized_access(client: Client, user1):
    """
    Test that the view is unavailable if user does not have proper rights to the stock user's user
    """
    client.force_login(user1)
    response = client.get(reverse("management:user:add"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_add_view_unauthorized_staff_access(client: Client, user4):
    """
    Test that a staff member without permissions cannot access the view
    """
    client.force_login(user4)
    response = client.get(reverse("management:user:add"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_add_view_authenticated_access(client: Client, user2):
    """
    Test that the view is unavailable if user does not have proper rights to the stock user's user
    """
    client.force_login(user2)
    response = client.get(reverse("management:user:add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_edit_view_unauthenticated_access(client: Client, user1):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("management:user:edit", args=[user1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_edit_view_unauthorized_access(client: Client, user1):
    """
    Test that the view is unavailable if user does not have proper rights to the stock user's user
    """
    client.force_login(user1)
    response = client.get(reverse("management:user:edit", args=[user1.pk]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_edit_view_unauthorized_staff_access(client: Client, user1, user4):
    """
    Test that a staff member without permissions cannot access the view
    """
    client.force_login(user4)
    response = client.get(reverse("management:user:edit", args=[user1.pk]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_edit_view_authenticated_access(client: Client, user1, user2):
    """
    Test that the view is unavailable if user does not have proper rights to the stock user's user
    """
    client.force_login(user2)
    response = client.get(reverse("management:user:edit", args=[user1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_delete_view_unauthenticated_access(client: Client, user1):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("management:user:delete", args=[user1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_delete_view_unauthorized_access(client: Client, user1, user2):
    """
    Test that the view is unavailable if user does not have proper rights to the stock user's user
    """
    client.force_login(user1)
    response = client.get(reverse("management:user:delete", args=[user1.pk]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_delete_view_unauthorized_staff_access(client: Client, user1, user4):
    """
    Test that a staff member without permissions cannot access the view
    """
    client.force_login(user4)
    response = client.get(reverse("management:user:delete", args=[user1.pk]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_delete_view_authenticated_access(client: Client, user1, user2):
    """
    Test that the view is unavailable if user does not have proper rights to the stock user's user
    """
    client.force_login(user2)
    response = client.get(reverse("management:user:delete", args=[user1.pk]))
    assert response.status_code == 200
