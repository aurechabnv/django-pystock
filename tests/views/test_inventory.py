import pytest
from django.test import Client
from django.urls import reverse

from apps.inventory.models import Movement, Stock


def test_inventory_view_get_unauthorized(client: Client):
    response = client.get(reverse("stock:list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_add_view_get_unauthorized(client: Client):
    response = client.get(reverse("stock:add"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_edit_view_get_unauthorized(client: Client, stock1):
    response = client.get(reverse("stock:edit", args=[stock1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_delete_view_get_unauthorized(client: Client, stock1):
    response = client.get(reverse("stock:delete", args=[stock1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_inventory_view_get(client: Client, user1, stock1, stock2, stock3):
    client.force_login(user1)
    response = client.get(reverse("stock:list"))
    assert response.context.get("stocks").count() == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_view_get_for_superuser(client: Client, user2, stock1, stock2, stock3):
    client.force_login(user2)
    response = client.get(reverse("stock:list"))
    assert response.context.get("stocks").count() == 3
    assert response.status_code == 200


@pytest.mark.django_db
def test_catalog_view_get_filter(client: Client, user1, stock1, stock2, stock3):
    client.force_login(user1)
    response = client.get(reverse("stock:list"), {"q": "tilleuls"})
    assert response.context.get("stocks").count() == 1
    assert "filters" in response.context
    assert "q" in response.context.get("filters")
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_add_view_get(client: Client, user1):
    client.force_login(user1)
    response = client.get(reverse("stock:add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_add_view_post_error(client: Client, user1, stock1):
    client.force_login(user1)
    incorrect_data = {"quantity": -5}
    response = client.post(reverse("stock:add"), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_get(client: Client, user1, stock1):
    client.force_login(user1)
    response = client.get(reverse("stock:edit", args=[stock1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_delete_view_get(client: Client, user1, stock1):
    client.force_login(user1)
    response = client.get(reverse("stock:delete", args=[stock1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_error(client: Client, user1, stock1):
    client.force_login(user1)
    incorrect_data = {"quantity": -5}
    response = client.post(reverse("stock:edit", args=[stock1.pk]), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_success(client: Client, user1, stock1, stock2):
    changed_data = {
        "type": Movement.MovementType.TRANSFER,
        "product": stock1.product.id,
        "from_location": stock2.location.id,
        "to_location": stock1.location.id,
        "quantity": 20,
    }
    client.force_login(user1)
    response = client.post(reverse("stock:edit", args=[stock2.id]), data=changed_data)
    stock1 = Stock.objects.get(id=stock1.id)
    stock2 = Stock.objects.get(id=stock2.id)
    assert stock1.quantity == 80
    assert stock2.quantity == 100
    assert response.status_code == 302
