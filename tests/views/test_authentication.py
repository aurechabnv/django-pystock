import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_login_view_get(client: Client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assertTemplateUsed(response, "account/login.html")


@pytest.mark.django_db
def test_password_change_view_get(client: Client, user1):
    client.force_login(user1)
    response = client.get(reverse('password_change'))
    assert response.status_code == 200
    assertTemplateUsed(response, "account/password_change.html")


def test_password_reset_view_get(client: Client):
    response = client.get(reverse('password_reset'))
    assert response.status_code == 200
    assertTemplateUsed(response, "account/password_reset.html")
