from django.contrib import admin

from apps.catalog.forms import CategoryForm, ProductForm
from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

    form = CategoryForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price', 'vat', 'stock_threshold')
    list_editable = ('price', 'vat', 'stock_threshold',)
    search_fields = ('name', 'sku')

    form = ProductForm
    filter_horizontal = ('categories',)
