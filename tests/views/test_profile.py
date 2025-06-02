import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


User = get_user_model()


def test_profile_view_get_unauthorized(client: Client):
    response = client.get(reverse("account:profile"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_view_get(client: Client, user1):
    client.force_login(user1)
    response = client.get(reverse("account:profile"))
    assert response.status_code == 200
    assertTemplateUsed(response, "account/profile.html")


@pytest.mark.django_db
def test_profile_view_post_error(client: Client, user1, user2):
    client.force_login(user1)
    incorrect_data = {"username": user2.username, "email": user1.email}
    response = client.post(reverse("account:profile"), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "username" in errors
    assert "unavailable_username" in [e.code for e in errors["username"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view_post_nochange(client: Client, user1):
    client.force_login(user1)
    unchanged_data = {"username": user1.username, "email": user1.email}
    response = client.post(reverse("account:profile"), data=unchanged_data)
    errors = response.context["form"].errors.as_data()
    assert not errors
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view_post_success(client: Client, user1):
    client.force_login(user1)
    changed_data = {"username": "another_name", "email": "name@example.com"}
    response = client.post(reverse("account:profile"), data=changed_data)
    user = User.objects.get(pk=user1.pk)
    assert user.username == changed_data.get("username")
    assert user.email == changed_data.get("email")
    assert response.status_code == 200
