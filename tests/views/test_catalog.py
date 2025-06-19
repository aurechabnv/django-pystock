import pytest
from django.test import Client
from django.urls import reverse

from apps.catalog.models import Product


def test_catalog_view_unauthenticated_access(client: Client):
    response = client.get(reverse("product:list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_catalog_view_authenticated_access(client: Client, user1, product1, product2):
    client.force_login(user1)
    response = client.get(reverse("product:list"))
    assert response.context.get("products").count() == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_catalog_view_query_filter(client: Client, user1, product1, product2):
    client.force_login(user1)
    response = client.get(reverse("product:list"), {"q": "gpu"})
    assert response.context.get("products").count() == 1
    assert "filters" in response.context
    assert "q" in response.context.get("filters")
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_add_view_unauthenticated_access(client: Client):
    response = client.get(reverse("product:add"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_product_add_view_authenticated_access(client: Client, user1):
    client.force_login(user1)
    response = client.get(reverse("product:add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_edit_view_unauthenticated_access(client: Client, product1):
    response = client.get(reverse("product:edit", args=[product1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_product_edit_view_authenticated_access(client: Client, user1, product1):
    client.force_login(user1)
    response = client.get(reverse("product:edit", args=[product1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_edit_view_post_error(client: Client, user1, product1, product2):
    client.force_login(user1)
    incorrect_data = {"sku": product2.sku}
    response = client.post(reverse("product:edit", args=[product1.pk]), data=incorrect_data)
    errors = response.context["form"].errors.as_data()
    assert "sku" in errors
    assert "unavailable_sku" in [e.code for e in errors["sku"]]
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_edit_view_post_success(client: Client, user1, product1):
    client.force_login(user1)
    changed_data = {
        "sku": "coucou",
        "name": product1.name,
        "price": product1.price,
        "vat": product1.vat,
        "stock_threshold": product1.stock_threshold,
        "categories": [c.pk for c in product1.categories.all()]
    }
    response = client.post(reverse("product:edit", args=[product1.pk]), data=changed_data)
    product = Product.objects.get(pk=product1.pk)
    categories = [c.pk for c in product.categories.all()]
    assert product.sku == changed_data.get("sku").upper()
    assert categories == changed_data.get("categories")
    assert response.status_code == 302


@pytest.mark.django_db
def test_product_delete_view_unauthenticated_access(client: Client, product1):
    response = client.get(reverse("product:delete", args=[product1.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_product_delete_view_authenticated_access(client: Client, user1, product1):
    client.force_login(user1)
    response = client.get(reverse("product:delete", args=[product1.pk]))
    assert response.status_code == 200
