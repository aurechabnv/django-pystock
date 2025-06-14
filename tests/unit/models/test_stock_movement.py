import pytest

from apps.inventory.models import Stock, Movement


@pytest.mark.django_db
def test_stock_creation(product2, location2):
    """
    Check that the stock creation works as expected.
    """
    stock = Stock(location=location2, product=product2, quantity=35)
    assert str(stock) == "MY-OTHER-PRODUCT - Great Place for Computer Parts - Entrepot des tilleuls (Entrepôt)"
    assert stock.last_modified is None
    stock.save()
    assert len(Movement.objects.all()) == 1
    latest_movement = Movement.objects.filter(product=product2).last()
    assert latest_movement.type == Movement.MovementType.INBOUND
    assert latest_movement.quantity == 35
    assert latest_movement.to_location == location2


@pytest.mark.django_db
def test_stock_update(stock1):
    """
    Check that the stock update works as expected.
    """
    stock_modified_date = stock1.last_modified
    last_movement = Movement.objects.all().last()
    stock1.quantity -= 5
    stock1.save()
    movements = Movement.objects.all()
    assert movements.count() == 2
    latest_movement = movements.last()
    assert stock_modified_date < stock1.last_modified
    assert last_movement.date < latest_movement.date
    assert latest_movement.type == Movement.MovementType.OUTBOUND
    assert latest_movement.quantity == -5
    assert latest_movement.from_location == stock1.location


@pytest.mark.django_db
def test_stock_outbound_updates(product1, location1, stock1, movement_outbound):
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
def test_stock_inbound_updates(product1, location2, stock2, movement_inbound):
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
def test_stock_transfer_updates(product1, location2, location1, stock2, movement_transfer):
    """
    Check that the stocks are properly updated on transfer and do not produce additional movement items.

    Additionally, the target location is set as new and without existing stock, so that we check that
    this use case does not produce additional movement either.
    """
    total_movements = Movement.objects.all().count()
    movement_transfer.synced = False
    movement_transfer.save()

    assert str(movement_transfer) == f"Transfert du {movement_transfer.date.strftime('%d-%m-%Y %H:%M')}"
    from_stock = Stock.objects.get(location=movement_transfer.from_location, product=movement_transfer.product)
    to_stock = Stock.objects.get(location=movement_transfer.to_location, product=movement_transfer.product)
    assert from_stock.quantity == 100
    assert to_stock.quantity == 20
    assert total_movements == Movement.objects.all().count()
