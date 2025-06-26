from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.inventory.forms import MovementForm
from apps.inventory.models import Stock, Movement


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'quantity', 'link_to_product', 'link_to_location',)
    search_fields = ('product__name', 'product__sku', 'location__name', 'location__siret', 'location__company__name', 'location__company__siret',)
    list_filter = ('location__type',)

    fields = ('location', 'product', 'quantity',)
    autocomplete_fields = ('location', 'product',)

    def link_to_product(self, obj):
        link = reverse("admin:catalog_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product)
    link_to_product.short_description = 'Product'

    def link_to_location(self, obj):
        link = reverse("admin:management_location_change", args=[obj.location.id])
        return format_html('<a href="{}">{}</a>', link, obj.location)
    link_to_location.short_description = 'Location'


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'quantity', 'product', 'from_location', 'to_location',)
    list_filter = ('type', 'date',)
    search_fields = ('product__name', 'from_location__name', 'to_location__name',)

    form = MovementForm
    autocomplete_fields = ('product', 'to_location', 'from_location',)
