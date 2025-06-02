import pytest


@pytest.mark.django_db
def test_company(company):
    """
    Check that the company model works as expected.
    """
    assert str(company) == "Great Place for Computer Parts [12345678912345]"


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

