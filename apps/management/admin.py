from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.management.models import Company, Location


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'email', 'website',)
    search_fields = ('name', 'siret',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'siret', 'type', 'full_address', 'link_to_company',)
    search_fields = ('name', 'siret', 'company__name', 'company__siret',)
    list_filter = ('type', 'city',)

    autocomplete_fields = ('company',)

    def link_to_company(self, obj):
        link = reverse("admin:inventory_company_change", args=[obj.company.id])
        return format_html('<a href="{}">{}</a>', link, obj.company)
    link_to_company.short_description = 'Company'
