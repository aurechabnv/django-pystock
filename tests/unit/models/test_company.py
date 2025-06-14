import pytest


@pytest.mark.django_db
def test_company(company1):
    """
    Check that the company model works as expected.
    """
    assert str(company1) == "Great Place for Computer Parts [12345678912345]"


@pytest.mark.django_db
def test_company_deletion(product1, company1, location2, location1, stock2, stock1,
                          movement_transfer, movement_inbound, movement_outbound):
    """
    Check that the company deletion cascades properly.
    """
    total, items = company1.delete()
    assert total == 11
    assert items['inventory.Company'] == 1
    assert items['inventory.Location'] == 2
    assert items['inventory.Stock'] == 2
    assert items['inventory.Movement'] == 5
    assert items['inventory.Company_users'] == 1

