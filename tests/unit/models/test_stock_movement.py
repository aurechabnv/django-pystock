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
def test_stock_outbound_updates(product1, location1, stock1, movement3_out):
    """
    Check that the stock is properly updated on outbound and does not produce an additional movement item.
    """
    total_movements = Movement.objects.all().count()
    movement3_out.synced = False
    movement3_out.save()

    assert str(movement3_out) == f"Sortie du {movement3_out.date.strftime('%d-%m-%Y %H:%M')}"
    from_stock = Stock.objects.get(location=movement3_out.from_location, product=movement3_out.product)
    assert from_stock.quantity == 25
    assert total_movements == Movement.objects.all().count()


@pytest.mark.django_db
def test_stock_inbound_updates(product1, location2, stock2, movement2_in):
    """
    Check that the stock is properly updated on inbound and does not produce an additional movement item.
    """
    total_movements = Movement.objects.all().count()
    movement2_in.synced = False
    movement2_in.save()

    assert str(movement2_in) == f"Entrée du {movement2_in.date.strftime('%d-%m-%Y %H:%M')}"
    to_stock = Stock.objects.get(location=movement2_in.to_location, product=movement2_in.product)
    assert to_stock.quantity == 220
    assert total_movements == Movement.objects.all().count()


@pytest.mark.django_db
def test_stock_transfer_updates(product1, location2, location1, stock2, movement1_tr):
    """
    Check that the stocks are properly updated on transfer and do not produce additional movement items.

    Additionally, the target location is set as new and without existing stock, so that we check that
    this use case does not produce additional movement either.
    """
    total_movements = Movement.objects.all().count()
    movement1_tr.synced = False
    movement1_tr.save()

    assert str(movement1_tr) == f"Transfert du {movement1_tr.date.strftime('%d-%m-%Y %H:%M')}"
    from_stock = Stock.objects.get(location=movement1_tr.from_location, product=movement1_tr.product)
    to_stock = Stock.objects.get(location=movement1_tr.to_location, product=movement1_tr.product)
    assert from_stock.quantity == 100
    assert to_stock.quantity == 20
    assert total_movements == Movement.objects.all().count()
