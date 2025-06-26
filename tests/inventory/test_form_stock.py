import pytest

from apps.inventory.forms import StockForm


@pytest.mark.django_db
def test_stock_form_filter_location_field_user(user1, location1, location2, location3):
    """
    Test that the location field are filtered based on user company rights
    """
    form = StockForm(user=user1)
    queryset = form.fields["location"].queryset
    assert queryset.count() == 2
    assert location3 not in queryset


@pytest.mark.django_db
def test_stock_form_filter_location_field_superuser(user2, location1, location2, location3):
    """
    Test that the location field are not filtered for a superuser
    """
    form = StockForm(user=user2)
    assert form.fields["location"].queryset.count() == 3
