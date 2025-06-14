import pytest

from apps.catalog.models import Category, Product


@pytest.mark.django_db
def test_category():
    """
    Check that the category model works as expected.
    """
    category = Category(name="Test Category")
    assert str(category) == "Test Category"
    assert category.slug == ""
    category.save()
    assert category.slug == "test-category"


@pytest.mark.django_db
def test_product():
    """
    Check that the product model works as expected.
    """
    product = Product(name="Test Product", sku="test-product", price=15.0, stock_threshold=10)
    assert str(product) == "Test Product [test-product]"
    assert product.vat == 0.2
    product.vat = 0.1
    product.save()
    assert str(product) == "Test Product [TEST-PRODUCT]"
    assert product.vat == 0.1


@pytest.mark.django_db
def test_product_categories(product1):
    """
    Check that the product method get_categories works as expected.
    """
    assert product1.get_categories() == "Composants PC, Cartes graphiques"


@pytest.mark.django_db
def test_product_deletion(product1, stock2, stock1,
                          movement_inbound, movement_outbound, movement_transfer):
    """
    Check that the product deletion cascades properly.
    """
    total, items = product1.delete()
    assert total == 10
    assert items['catalog.Product'] == 1
    assert items['catalog.Product_categories'] == 2
    assert items['inventory.Stock'] == 2
    assert items['inventory.Movement'] == 5
