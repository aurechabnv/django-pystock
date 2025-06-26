import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_home_view_authenticated_user(client, user1):
    client.force_login(user1)
    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse("stock:list")


@pytest.mark.django_db
def test_home_view_authenticated_staff(client, user2):
    client.force_login(user2)
    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse("dashboard")
