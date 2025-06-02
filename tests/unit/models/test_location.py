import pytest


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
