import pytest

from apps.catalog.models import Category, Product
from apps.inventory.models import Stock, Company, Movement, Location


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
def test_company(company):
    """
    Check that the company model works as expected.
    """
    assert str(company) == "Great Place for Computer Parts [12345678912345]"


@pytest.mark.django_db
def test_location(shop):
    """
    Check that the location model works as expected.
    """
    assert str(shop) == "Great Place for Computer Parts - GPCP Montpellier"
    shop.siret = "32543442257446"
    assert str(shop) == "Great Place for Computer Parts - GPCP Montpellier [32543442257446]"
    assert shop.full_address == "45 rue des peupliers, 34000 Montpellier"
    shop.address_line_2 = "info"
    assert shop.full_address == "45 rue des peupliers, info, 34000 Montpellier"


@pytest.mark.django_db
def test_stock_creation(product2, warehouse):
    """
    Check that the stock creation works as expected.
    """
    stock = Stock(location=warehouse, product=product2, quantity=35)
    assert str(stock) == "MY-OTHER-PRODUCT - Great Place for Computer Parts - Entrepot des tilleuls (Entrepôt)"
    assert stock.last_modified is None
    stock.save()
    assert len(Movement.objects.all()) == 1
    latest_movement = Movement.objects.filter(product=product2).last()
    assert latest_movement.type == Movement.MovementType.INBOUND
    assert latest_movement.quantity == 35
    assert latest_movement.to_location == warehouse


@pytest.mark.django_db
def test_stock_update(stock_in_shop):
    """
    Check that the stock update works as expected.
    """
    stock_modified_date = stock_in_shop.last_modified
    last_movement = Movement.objects.all().last()
    stock_in_shop.quantity -= 5
    stock_in_shop.save()
    movements = Movement.objects.all()
    assert movements.count() == 2
    latest_movement = movements.last()
    assert stock_modified_date < stock_in_shop.last_modified
    assert last_movement.date < latest_movement.date
    assert latest_movement.type == Movement.MovementType.OUTBOUND
    assert latest_movement.quantity == -5
    assert latest_movement.from_location == stock_in_shop.location


@pytest.mark.django_db
def test_stock_outbound_updates(product1, shop, stock_in_shop, movement_outbound):
    """
    Check that the stock is properly updated on outbound and does not produce an additional movement item.
    """
    total_movements = Movement.objects.all().count()
    movement_outbound.synced = False
    movement_outbound.save()

    assert str(movement_outbound) == f"Sortie du {movement_outbound.date.strftime('%d-%m-%Y %H:%M')}"
    from_stock = Stock.objects.get(location=movement_outbound.from_location, product=movement_outbound.product)
    assert from_stock.quantity == 25
    assert total_movements == Movement.objects.all().count()


@pytest.mark.django_db
def test_stock_inbound_updates(product1, warehouse, stock_in_warehouse, movement_inbound):
    """
    Check that the stock is properly updated on inbound and does not produce an additional movement item.
    """
    total_movements = Movement.objects.all().count()
    movement_inbound.synced = False
    movement_inbound.save()

    assert str(movement_inbound) == f"Entrée du {movement_inbound.date.strftime('%d-%m-%Y %H:%M')}"
    to_stock = Stock.objects.get(location=movement_inbound.to_location, product=movement_inbound.product)
    assert to_stock.quantity == 220
    assert total_movements == Movement.objects.all().count()


@pytest.mark.django_db
def test_stock_transfer_updates(product1, warehouse, shop, stock_in_shop, stock_in_warehouse,
                                movement_transfer):
    """
    Check that the stocks are properly updated on transfer and do not produce additional movement items.
    """
    total_movements = Movement.objects.all().count()
    movement_transfer.synced = False
    movement_transfer.save()

    assert str(movement_transfer) == f"Transfert du {movement_transfer.date.strftime('%d-%m-%Y %H:%M')}"
    from_stock = Stock.objects.get(location=movement_transfer.from_location, product=movement_transfer.product)
    to_stock = Stock.objects.get(location=movement_transfer.to_location, product=movement_transfer.product)
    assert from_stock.quantity == 100
    assert to_stock.quantity == 80
    assert total_movements == Movement.objects.all().count()


@pytest.mark.django_db
def test_product_deletion(product1, stock_in_warehouse, stock_in_shop,
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


@pytest.mark.django_db
def test_company_deletion(product1, company, warehouse, shop, stock_in_warehouse, stock_in_shop,
                          movement_transfer, movement_inbound, movement_outbound):
    """
    Check that the company deletion cascades properly.
    """
    total, items = company.delete()
    assert total == 10
    assert items['inventory.Company'] == 1
    assert items['inventory.Location'] == 2
    assert items['inventory.Stock'] == 2
    assert items['inventory.Movement'] == 5


@pytest.mark.django_db
def test_location_deletion(product1, company, shop, stock_in_shop, stock_in_warehouse,
                           movement_transfer, movement_inbound, movement_outbound):
    """
    Check that the location deletion cascades properly.
    """
    total, items = shop.delete()
    assert total == 5
    assert items['inventory.Location'] == 1
    assert items['inventory.Stock'] == 1
    assert items['inventory.Movement'] == 3
