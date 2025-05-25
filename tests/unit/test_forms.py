import pytest

from apps.inventory.forms import MovementForm
from apps.inventory.models import Movement


MOVEMENT_FORM_DATA = {
    "product": "1",
    "quantity": 5,
    "from_location": "1",
    "to_location": "2",
}


def test_movement_form_inbound_mandatory_field():
    """
    Test that only the `to_location` field is mandatory
    when the `type` is INBOUND
    """
    form = MovementForm(data={"type": Movement.MovementType.INBOUND})
    assert form.is_valid() == False
    assert "to_location" in form.errors
    assert "from_location" not in form.errors


def test_movement_form_outbound_mandatory_field():
    """
    Test that only the `from_location` field is mandatory
    when the `type` is OUTBOUND
    """
    form = MovementForm(data={"type": Movement.MovementType.OUTBOUND})
    assert form.is_valid() == False
    assert "from_location" in form.errors
    assert "to_location" not in form.errors


def test_movement_form_transfer_mandatory_fields():
    """
    Test that both `to_location` and `from_location` fields are mandatory
    when the `type` is TRANSFER
    """
    form = MovementForm(data={"type": Movement.MovementType.TRANSFER})
    assert form.is_valid() == False
    assert "from_location" in form.errors
    assert "to_location" in form.errors


@pytest.mark.django_db
def test_movement_form_inbound(product1, shop, warehouse):
    """
    Test that the unnecessary `from_location` field is cleared
    when the `type` is INBOUND
    """
    data = MOVEMENT_FORM_DATA.copy()
    data["type"] = Movement.MovementType.INBOUND
    form = MovementForm(data)
    assert form.is_valid() == True
    assert form.cleaned_data["from_location"] is None


@pytest.mark.django_db
def test_movement_form_outbound(product1, shop, warehouse):
    """
    Test that the unnecessary `to_location` field is cleared
    when the `type` is OUTBOUND
    """
    data = MOVEMENT_FORM_DATA.copy()
    data["type"] = Movement.MovementType.OUTBOUND
    form = MovementForm(data)
    assert form.is_valid() == True
    assert form.cleaned_data["to_location"] is None
