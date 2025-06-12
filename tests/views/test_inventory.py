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
def test_stock_edit_view_get_unauthorized(client: Client, stock_in_shop):
    response = client.get(reverse("stock:edit", args=[stock_in_shop.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_delete_view_get_unauthorized(client: Client, stock_in_shop):
    response = client.get(reverse("stock:delete", args=[stock_in_shop.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_inventory_view_get(client: Client, user1, stock_in_shop, stock_in_warehouse):
    client.force_login(user1)
    response = client.get(reverse("stock:list"))
    assert response.context.get("stocks").count() == 2
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_catalog_view_get_filter(client: Client, user1, product1, product2):
#     client.force_login(user1)
#     response = client.get(reverse("stock:list"), {"q": "gpu"})
#     assert response.context.get("stocks").count() == 1
#     assert "filters" in response.context
#     assert "q" in response.context.get("filters")
#     assert response.status_code == 200


@pytest.mark.django_db
def test_stock_add_view_get(client: Client, user1):
    client.force_login(user1)
    response = client.get(reverse("stock:add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_add_view_post_error(client: Client, user1, stock_in_shop):
    client.force_login(user1)
    incorrect_data = {"quantity": -5}
    response = client.post(reverse("stock:add"), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_get(client: Client, user1, stock_in_shop):
    client.force_login(user1)
    response = client.get(reverse("stock:edit", args=[stock_in_shop.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_delete_view_get(client: Client, user1, stock_in_shop):
    client.force_login(user1)
    response = client.get(reverse("stock:delete", args=[stock_in_shop.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_error(client: Client, user1, stock_in_shop):
    client.force_login(user1)
    incorrect_data = {"quantity": -5}
    response = client.post(reverse("stock:edit", args=[stock_in_shop.pk]), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_success(client: Client, user1, product1, shop, warehouse, stock_in_shop, stock_in_warehouse):
    changed_data = {
        "type": Movement.MovementType.TRANSFER,
        "product": stock_in_shop.product.id,
        "from_location": stock_in_warehouse.location.id,
        "to_location": stock_in_shop.location.id,
        "quantity": 20,
    }
    client.force_login(user1)
    response = client.post(reverse("stock:edit", args=[stock_in_warehouse.pk]), data=changed_data)
    stock1 = Stock.objects.get(pk=stock_in_warehouse.pk)
    stock2 = Stock.objects.get(pk=stock_in_shop.pk)
    assert stock1.quantity == 100
    assert stock2.quantity == 80
    assert response.status_code == 302
