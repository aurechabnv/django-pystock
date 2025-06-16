import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


User = get_user_model()


VALID_SIGNUP_DATA = {
    "username": "sandra",
    "email": "sandra@robbins.com",
    "password1": "Pa$$word123",
    "password2": "Pa$$word123",
}


def test_register_view_get(client: Client):
    response = client.get(reverse("register"))
    assert response.status_code == 200
    assertTemplateUsed(response, "account/register.html")


@pytest.mark.django_db
def test_register_view_post(client: Client):
    response = client.post(reverse("register"), data=VALID_SIGNUP_DATA)
    user = User.objects.get(username=VALID_SIGNUP_DATA["username"])
    assert user.is_authenticated
    assert response.status_code == 302


@pytest.mark.django_db
def test_register_view_password_mismatch(client: Client):
    incorrect_data = VALID_SIGNUP_DATA.copy()
    incorrect_data["password1"] = "whatever"
    response = client.post(reverse("register"), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "password2" in errors
    assert "password_mismatch" in [e.code for e in errors["password2"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view_password_length(client: Client):
    incorrect_data = VALID_SIGNUP_DATA.copy()
    incorrect_data["password1"] = "azerty"
    incorrect_data["password2"] = "azerty"
    response = client.post(reverse("register"), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "password2" in errors
    assert "password_too_short" in [e.code for e in errors["password2"]]
    assert response.status_code == 200
