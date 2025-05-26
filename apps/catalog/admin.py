from django.contrib import admin

from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price', 'vat', 'stock_threshold',)
    list_editable = ('price', 'vat', 'stock_threshold',)
    search_fields = ('name', 'sku',)

    filter_horizontal = ('categories',)
