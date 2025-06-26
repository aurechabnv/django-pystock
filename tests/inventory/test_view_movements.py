import pytest
from django.test import Client
from django.urls import reverse


def test_history_view_unauthenticated_access(client: Client):
    response = client.get(reverse("stock:movements"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_history_view_unauthorized_access(client: Client, user3):
    client.force_login(user3)
    response = client.get(reverse("stock:movements"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_history_view_authenticated_access_user(client: Client, user1, movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user1)
    response = client.get(reverse("stock:movements"))
    objects = response.context.get("object_list")
    assert objects.count() == 3
    assert movement4 not in objects
    assert response.status_code == 200


@pytest.mark.django_db
def test_history_view_authenticated_access_superuser(client: Client, user2, movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user2)
    response = client.get(reverse("stock:movements"))
    assert response.context.get("object_list").count() == 4
    assert response.status_code == 200


@pytest.mark.django_db
def test_history_view_query_filter(client: Client, user1, movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user1)
    response = client.get(reverse("stock:movements"), {"q": "tilleuls"})
    objects = response.context.get("object_list")
    assert objects.count() == 2
    assert movement1_tr in objects
    assert movement2_in in objects
    assert "filters" in response.context
    assert "q" in response.context.get("filters")
    assert response.status_code == 200


@pytest.mark.django_db
def test_history_view_product_location_filter(client: Client, user1, product1, location1,
                                 movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user1)
    response = client.get(reverse("stock:movements"), {"p": product1.id, "l": location1.id})
    objects = response.context.get("object_list")
    assert objects.count() == 2
    assert movement1_tr in objects
    assert movement3_out in objects
    assert "filters" in response.context
    assert response.context.get("filters").get("product") == str(product1)
    assert response.context.get("filters").get("location") == str(location1)
    assert response.status_code == 200
