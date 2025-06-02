import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_home(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")
