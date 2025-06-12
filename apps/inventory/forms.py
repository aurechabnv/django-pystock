from django import forms
from django.core.exceptions import ValidationError

from apps.inventory.models import Movement, Stock


def validate_quantity(instance, error_message):
    quantity = instance.cleaned_data.get("quantity")
    if quantity < 0:
        raise forms.ValidationError(message=error_message, code="invalid_qty")
    return quantity


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["product", "location", "quantity"]

    def clean_quantity(self):
        return validate_quantity(self, "La quantité doit être supérieure ou égale à zéro.")


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = [
            "type",
            "product",
            "from_location",
            "to_location",
            "quantity",
        ]

    def clean_quantity(self):
        return validate_quantity(self, "La quantité doit être supérieure à zéro.")

    def clean(self):
        cleaned_data = super().clean()
        movement_type = cleaned_data.get("type")
        to_location = cleaned_data.get("to_location")
        from_location = cleaned_data.get("from_location")

        # Check that the proper locations are set based on the movement type
        error = ValidationError("Ce champ est obligatoire.", code="required")
        if movement_type != Movement.MovementType.INBOUND:
            if not from_location:
                self.add_error('from_location', error)

        if movement_type != Movement.MovementType.OUTBOUND:
            if not to_location:
                self.add_error('to_location', error)

        # Ensure data consistency by clearing unnecessary fields
        if movement_type == Movement.MovementType.INBOUND:
            if from_location:
                self.cleaned_data['from_location'] = None
        if movement_type == Movement.MovementType.OUTBOUND:
            if to_location:
                self.cleaned_data['to_location'] = None

        return self.cleaned_data
