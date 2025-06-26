import pytest

from apps.inventory.forms import MovementForm
from apps.inventory.models import Movement


MOVEMENT_FORM_DATA = {
    "product": "1",
    "quantity": 5,
    "from_location": "1",
    "to_location": "2",
}


@pytest.mark.django_db
def test_movement_form_inbound_mandatory_field(user1):
    """
    Test that only the `to_location` field is mandatory
    when the `type` is INBOUND
    """
    form = MovementForm(data={"type": Movement.MovementType.INBOUND}, user=user1)
    assert form.is_valid() == False
    assert "to_location" in form.errors
    assert "from_location" not in form.errors


@pytest.mark.django_db
def test_movement_form_outbound_mandatory_field(user1):
    """
    Test that only the `from_location` field is mandatory
    when the `type` is OUTBOUND
    """
    form = MovementForm(data={"type": Movement.MovementType.OUTBOUND}, user=user1)
    assert form.is_valid() == False
    assert "from_location" in form.errors
    assert "to_location" not in form.errors


@pytest.mark.django_db
def test_movement_form_transfer_mandatory_fields(user1):
    """
    Test that both `to_location` and `from_location` fields are mandatory
    when the `type` is TRANSFER
    """
    form = MovementForm(data={"type": Movement.MovementType.TRANSFER}, user=user1)
    assert form.is_valid() == False
    assert "from_location" in form.errors
    assert "to_location" in form.errors


@pytest.mark.django_db
def test_movement_form_inbound_cleaned(product1, location1, location2, user1):
    """
    Test that the unnecessary `from_location` field is cleared
    when the `type` is INBOUND
    """
    data = MOVEMENT_FORM_DATA.copy()
    data["type"] = Movement.MovementType.INBOUND
    form = MovementForm(data, user=user1)
    assert form.is_valid() == True
    assert form.cleaned_data["from_location"] is None


@pytest.mark.django_db
def test_movement_form_outbound_cleaned(product1, location1, location2, user1):
    """
    Test that the unnecessary `to_location` field is cleared
    when the `type` is OUTBOUND
    """
    data = MOVEMENT_FORM_DATA.copy()
    data["type"] = Movement.MovementType.OUTBOUND
    form = MovementForm(data, user=user1)
    assert form.is_valid() == True
    assert form.cleaned_data["to_location"] is None


@pytest.mark.django_db
def test_movement_form_filter_location_fields_user(user1, product1, location1, location2, location3):
    """
    Test that the location fields are filtered based on user company rights
    """
    data = MOVEMENT_FORM_DATA.copy()
    data["type"] = Movement.MovementType.TRANSFER
    form = MovementForm(user=user1)
    queryset = form.fields["to_location"].queryset
    assert queryset.count() == 2
    assert location3 not in queryset


@pytest.mark.django_db
def test_movement_form_filter_location_fields_superuser(user2, product1, location1, location2, location3):
    """
    Test that the location fields are not filtered for a superuser
    """
    data = MOVEMENT_FORM_DATA.copy()
    data["type"] = Movement.MovementType.TRANSFER
    form = MovementForm(user=user2)
    assert form.fields["to_location"].queryset.count() == 3
