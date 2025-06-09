from django import forms

from apps.catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_sku(self):
        value = self.cleaned_data.get('sku')
        if Product.objects.exclude(pk__exact=self.instance.pk).filter(sku=value).exists():
            raise forms.ValidationError(message="Ce SKU est déjà utilisé.", code="unavailable_sku")
        return value
