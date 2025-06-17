import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_dashboard_unauthenticated(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_authenticated(client, user1):
    client.force_login(user1)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'reporting/dashboard.html')
