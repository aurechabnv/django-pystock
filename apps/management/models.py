from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Raison sociale")
    siret = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=11, blank=True, verbose_name="Téléphone")
    website = models.URLField(blank=True, verbose_name="Site internet")
    email = models.EmailField(blank=True, verbose_name="Email de contact")
    users = models.ManyToManyField(User, blank=True, verbose_name="Utilisateurs", related_name="companies")
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "société"
        permissions = [
            ("company_update_stock", "Can update company stocks"),
            ("company_delete_stock", "Can delete company stocks"),
            ("company_add_stock", "Can add company stocks"),
        ]

    def __str__(self):
        return f"{self.name} [{self.siret}]"

    def location_count(self):
        count = defaultdict(int)
        for l in self.locations.all():
            count[l.type] += 1
        return count


class Location(models.Model):
    class LocationType(models.TextChoices):
        SHOP = "SH", "Magasin"
        WAREHOUSE = "WH", "Entrepôt"

    class Meta:
        verbose_name = "site"

    type = models.CharField(max_length=2, choices=LocationType)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Société", related_name="locations")
    name = models.CharField(max_length=100, verbose_name="Raison sociale")
    siret = models.CharField(max_length=14, blank=True, unique=True, null=True)
    address_line_1 = models.CharField(max_length=100, verbose_name="Adresse ligne 1")
    address_line_2 = models.CharField(max_length=100, blank=True, verbose_name="Adresse ligne 2")
    zip_code = models.CharField(max_length=10, verbose_name="Code postal")
    city = models.CharField(max_length=30, verbose_name="Ville")
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.name}{' [' + self.siret + ']' if self.siret else ''}"

    @property
    def full_address(self):
        return f"{self.address_line_1 + ', '}{self.address_line_2 + ', ' if self.address_line_2 else ''}{self.zip_code} {self.city}"
