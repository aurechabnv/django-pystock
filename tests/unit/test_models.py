import pytest

from apps.catalog.models import Category, Product
from apps.inventory.models import Stock, Company, Movement, Location


@pytest.mark.django_db
def test_category():
    category = Category(name="Test Category")
    assert str(category) == "Test Category"
    assert category.slug == ""
    category.save()
    assert category.slug == "test-category"


@pytest.mark.django_db
def test_product():
    product = Product(name="Test Product", sku="test-product", price=15.0, stock_threshold=10)
    assert str(product) == "Test Product"
    assert product.vat == 0.2
    product.vat = 0.3
    product.save()
    assert product.vat == 0.3


@pytest.mark.django_db
def test_company():
    company = Company(name='Great Place for Computer Parts', siret='12345678912345')
    assert str(company) == "Great Place for Computer Parts [12345678912345]"


@pytest.mark.django_db
def test_location():
    location = Location(name="Test Location", type=Location.LocationType.SHOP)
    assert str(location) == "Test Location (Shop)"


@pytest.mark.django_db
def test_stock(product_gpu, warehouse):
    stock = Stock(location=warehouse, product=product_gpu, quantity=35)
    assert str(stock) == "35x 'RADEON RX 9070 XT' (Entrepot des tilleuls)"
    assert stock.last_modified is None
    stock.save()
    assert stock.last_modified is not None


@pytest.mark.django_db
def test_stock_update(stock_in_shop):
    item_date = stock_in_shop.last_modified
    stock_in_shop.quantity += 1
    stock_in_shop.save()
    assert item_date < stock_in_shop.last_modified


@pytest.mark.django_db
def test_stock_outbound_updates(product_gpu, shop, stock_in_shop):
    movement = Movement(product=product_gpu, from_location=shop, quantity=10, type=Movement.MovementType.OUTBOUND)
    assert str(movement) == "10x 'RADEON RX 9070 XT' from 'GPCP Montpellier' (Outbound)"
    assert movement.date is None
    assert movement.to_location is None
    movement.save()
    assert movement.date is not None
    from_stock = Stock.objects.get(location=movement.from_location, product=movement.product)
    assert from_stock.quantity == 50


@pytest.mark.django_db
def test_stock_inbound_updates(product_gpu, warehouse, stock_in_warehouse):
    movement = Movement(product=product_gpu, to_location=warehouse, quantity=10, type=Movement.MovementType.INBOUND)
    assert str(movement) == "10x 'RADEON RX 9070 XT' to 'Entrepot des tilleuls' (Inbound)"
    assert movement.from_location is None
    movement.save()
    to_stock = Stock.objects.get(location=movement.to_location, product=movement.product)
    assert to_stock.quantity == 130


@pytest.mark.django_db
def test_stock_transfer_updates(product_gpu, warehouse, shop, stock_in_shop, stock_in_warehouse):
    movement = Movement(product=product_gpu, from_location=warehouse, to_location=shop, quantity=10,
                        type=Movement.MovementType.TRANSFER)
    assert str(movement) == "10x 'RADEON RX 9070 XT' from 'Entrepot des tilleuls' to 'GPCP Montpellier' (Transfer)"
    movement.save()
    from_stock = Stock.objects.get(location=movement.from_location, product=movement.product)
    to_stock = Stock.objects.get(location=movement.to_location, product=movement.product)
    assert from_stock.quantity == 110
    assert to_stock.quantity == 70


@pytest.mark.django_db
def test_product_deletion(product_gpu, stock_in_warehouse, stock_in_shop, movement_transfer, movement_inbound,
                          movement_outbound):
    total, items = product_gpu.delete()
    assert total == 8
    assert items['catalog.Product'] == 1
    assert items['catalog.Product_categories'] == 2
    assert items['inventory.Stock'] == 2
    assert items['inventory.Movement'] == 3


@pytest.mark.django_db
def test_company_deletion(product_gpu, company, warehouse, shop, stock_in_warehouse, stock_in_shop, movement_transfer,
                          movement_inbound, movement_outbound):
    total, items = company.delete()
    assert total == 8
    assert items['inventory.Company'] == 1
    assert items['inventory.Location'] == 2
    assert items['inventory.Stock'] == 2
    assert items['inventory.Movement'] == 3


@pytest.mark.django_db
def test_location_deletion(product_gpu, company, shop, stock_in_shop, stock_in_warehouse, movement_transfer,
                           movement_outbound):
    total, items = shop.delete()
    assert total == 4
    assert items['inventory.Location'] == 1
    assert items['inventory.Stock'] == 1
    assert items['inventory.Movement'] == 2
