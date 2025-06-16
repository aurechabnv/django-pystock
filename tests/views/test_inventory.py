import pytest
from django.test import Client
from django.urls import reverse

from apps.inventory.models import Movement, Stock


def test_inventory_view_unauthenticated_access(client: Client):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("stock:list"))
    assert response.status_code == 302


def test_stock_add_view_unauthenticated_access(client: Client):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("stock:add"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_edit_view_unauthenticated_access(client: Client, stock1):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("stock:edit", args=[stock1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_delete_view_unauthenticated_access(client: Client, stock1):
    """
    Test that a visitor cannot access the view without authentication
    """
    response = client.get(reverse("stock:delete", args=[stock1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_add_view_authenticated_access(client: Client, user1):
    """
    Test that an authenticated user can access the view
    """
    client.force_login(user1)
    response = client.get(reverse("stock:add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_authenticated_access(client: Client, user1, stock1):
    """
    Test that an authenticated user can access the view
    """
    client.force_login(user1)
    response = client.get(reverse("stock:edit", args=[stock1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_delete_view_authenticated_access(client: Client, user1, stock1):
    """
    Test that an authenticated user can access the view
    """
    client.force_login(user1)
    response = client.get(reverse("stock:delete", args=[stock1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_unauthorized_access(client: Client, user1, stock3):
    """
    Test that the view is unavailable if user does not have proper rights to the stock location's company
    """
    client.force_login(user1)
    response = client.get(reverse("stock:edit", args=[stock3.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_delete_unauthorized_access(client: Client, user1, stock3):
    """
    Test that the view is unavailable if user does not have proper rights to the stock location's company
    """
    client.force_login(user1)
    response = client.get(reverse("stock:delete", args=[stock3.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_stock_edit_view_authorized_access(client: Client, user2, stock3):
    """
    Test that the view is unavailable if user does not have proper rights to the stock location's company
    """
    client.force_login(user2)
    response = client.get(reverse("stock:edit", args=[stock3.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_delete_unauthorized_access(client: Client, user2, stock3):
    """
    Test that the view is unavailable if user does not have proper rights to the stock location's company
    """
    client.force_login(user2)
    response = client.get(reverse("stock:delete", args=[stock3.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_view_authenticated_access_user(client: Client, user1, stock1, stock2, stock3):
    """
    Test that an authenticated user can access the view
    and that the results are filtered based on user company rights
    """
    client.force_login(user1)
    response = client.get(reverse("stock:list"))
    assert response.context.get("stocks").count() == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_view_authenticated_access_superuser(client: Client, user2, stock1, stock2, stock3):
    """
    Test that an authenticated user can access the view
    and that the results are not filtered
    """
    client.force_login(user2)
    response = client.get(reverse("stock:list"))
    assert response.context.get("stocks").count() == 3
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_view_query_filter(client: Client, user1, stock1, stock2, stock3):
    """
    Test that the results can be filtered based on user search
    """
    client.force_login(user1)
    response = client.get(reverse("stock:list"), {"q": "tilleuls"})
    assert response.context.get("stocks").count() == 1
    assert "filters" in response.context
    assert "q" in response.context.get("filters")
    assert response.context.get("filters").get("q") == "tilleuls"
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_view_low_stock_filter(client: Client, user2, stock1, stock2, stock3):
    """
    Test that the results can be filtered based on user search
    """
    client.force_login(user2)
    response = client.get(reverse("stock:list"), {"low_stock": "on"})
    assert response.context.get("stocks").count() == 2
    assert "filters" in response.context
    assert "low_stock" in response.context.get("filters")
    assert response.context.get("filters").get("low_stock") == "on"
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_add_view_post_qty_error(client: Client, user1, stock1):
    """
    Test that a negative quantity value raises a form error
    """
    client.force_login(user1)
    incorrect_data = {"quantity": -5}
    response = client.post(reverse("stock:add"), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_zero_qty_error(client: Client, user1, stock1):
    """
    Test that zero quantity value raises a form error
    """
    client.force_login(user1)
    incorrect_data = {"quantity": 0}
    response = client.post(reverse("stock:edit", args=[stock1.pk]), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_negative_qty_error(client: Client, user1, stock1):
    """
    Test that a negative quantity value raises a form error
    """
    client.force_login(user1)
    incorrect_data = {"quantity": -5}
    response = client.post(reverse("stock:edit", args=[stock1.pk]), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "quantity" in errors
    assert "invalid_qty" in [e.code for e in errors["quantity"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_edit_view_post_success(client: Client, user1, stock1, stock2):
    """
    Test that submitting a valid form works properly
    """
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
