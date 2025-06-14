import pytest


@pytest.mark.django_db
def test_location(location1):
    """
    Check that the location model works as expected.
    """
    assert str(location1) == "Great Place for Computer Parts - GPCP Montpellier"
    location1.siret = "32543442257446"
    assert str(location1) == "Great Place for Computer Parts - GPCP Montpellier [32543442257446]"
    assert location1.full_address == "45 rue des peupliers, 34000 Montpellier"
    location1.address_line_2 = "info"
    assert location1.full_address == "45 rue des peupliers, info, 34000 Montpellier"


@pytest.mark.django_db
def test_location_deletion(product1, company1, location1, stock1, stock2,
                           movement_transfer, movement_inbound, movement_outbound):
    """
    Check that the location deletion cascades properly.
    """
    total, items = location1.delete()
    assert total == 5
    assert items['inventory.Location'] == 1
    assert items['inventory.Stock'] == 1
    assert items['inventory.Movement'] == 3
