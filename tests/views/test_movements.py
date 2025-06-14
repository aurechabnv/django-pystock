import pytest
from django.test import Client
from django.urls import reverse


def test_history_view_get_unauthorized(client: Client):
    response = client.get(reverse("stock:movements"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_history_view_get(client: Client, user1, movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user1)
    response = client.get(reverse("stock:movements"))
    assert response.context.get("object_list").count() == 3
    assert response.status_code == 200


@pytest.mark.django_db
def test_history_view_get_for_superuser(client: Client, user2, movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user2)
    response = client.get(reverse("stock:movements"))
    assert response.context.get("object_list").count() == 4
    assert response.status_code == 200


@pytest.mark.django_db
def test_history_view_get_filter(client: Client, user1, movement1_tr, movement2_in, movement3_out, movement4):
    client.force_login(user1)
    response = client.get(reverse("stock:movements"), {"q": "tilleuls"})
    assert response.context.get("object_list").count() == 2
    assert "filters" in response.context
    assert "q" in response.context.get("filters")
    assert response.status_code == 200
