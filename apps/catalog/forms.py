from django import forms

from apps.catalog.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        labels = {
            "name": "Nom de catégorie",
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "name": "Nom de produit",
            "sku": "Identifiant du produit",
            "price": "Prix",
            "vat": "TVA",
            "stock_threshold": "Alerte de stock",
            "categories": "Catégories",
        }
