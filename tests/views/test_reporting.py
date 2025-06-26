import json

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_dashboard_unauthenticated(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_unauthorized(client, user1):
    client.force_login(user1)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_dashboard_authenticated(client, user2):
    client.force_login(user2)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'reporting/dashboard.html')


def test_api_categories_unauthenticated(client):
    response = client.get(reverse('api_categories'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_api_categories_unauthorized(client, user1):
    client.force_login(user1)
    response = client.get(reverse('api_categories'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_api_categories_authenticated(client, user2, category1, category2, product1, product2):
    client.force_login(user2)
    response = client.get(reverse('api_categories'))
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content['labels'] == [category2.name, category1.name]
    assert content['data'] == [1, 1]


def test_api_stock_per_month_unauthenticated(client):
    response = client.get(reverse('api_stock_evolution'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_api_stock_per_month_unauthorized(client, user1):
    client.force_login(user1)
    response = client.get(reverse('api_stock_evolution'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_api_stock_per_month_authenticated(client, user2, stock1, stock2, stock3):
    client.force_login(user2)
    response = client.get(reverse('api_stock_evolution'))
    content = json.loads(response.content)
    assert response.status_code == 200
    assert len(content['labels']) == 1
    assert content['in'] == [235]
