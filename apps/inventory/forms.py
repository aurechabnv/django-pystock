from django import forms
from django.db import models
from django.core.exceptions import ValidationError

from apps.inventory.models import Movement, Location, Stock, Company


def urlfields_assume_https(db_field, **kwargs):
    """
    ModelForm.Meta.formfield_callback function to assume HTTPS for scheme-less
    domains in URLFields.
    """
    if isinstance(db_field, models.URLField):
        kwargs["assume_scheme"] = "https"
    return db_field.formfield(**kwargs)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "siret",
            "phone",
            "website",
            "email",
        ]
        labels = {
            "name": "Nom de société",
            "phone": "N° de téléphone",
        }
        formfield_callback = urlfields_assume_https


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "type",
            "company",
            "name",
            "siret",
            "address_line_1",
            "address_line_2",
            "zip_code",
            "city",
        ]
        labels = {
            "company": "Société",
            "name": "Nom du site",
            "siret": "N° de SIRET",
            "address_line_1": "Adresse ligne 1",
            "address_line_2": "Adresse ligne 2",
            "zip_code": "Code postal",
            "city": "Ville",
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            "location",
            "product",
            "quantity",
        ]
        labels = {
            "location": "Site",
            "product": "Produit",
            "quantity": "Quantité",
        }


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = [
            "type",
            "product",
            "quantity",
            "from_location",
            "to_location",
        ]
        labels = {
            "product": "Produit",
            "quantity": "Quantité",
            "from_location": "Origine",
            "to_location": "Destination",
        }

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
