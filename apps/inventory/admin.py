from django.contrib import admin

from apps.inventory.models import Company, Location, Stock, Movement


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    ...

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    ...

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    ...

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    ...
