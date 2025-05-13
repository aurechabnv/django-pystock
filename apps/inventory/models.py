from django.db import models

from apps.catalog.models import Product


class Company(models.Model):
    name = models.CharField(max_length=100)
    siret = models.CharField(max_length=14)
    phone = models.CharField(max_length=11, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    SHOP = 'SH'
    WAREHOUSE = 'WH'
    LOCATION_TYPE_CHOICES = [
        (SHOP, 'Shop'),
        (WAREHOUSE, 'Warehouse'),
    ]

    type = models.CharField(max_length=2, choices=LOCATION_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    siret = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Stock(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)


class Movement(models.Model):
    INBOUND = 'I'
    OUTBOUND = 'O'
    TRANSFER = 'T'
    MOVEMENT_TYPE_CHOICES = [
        (INBOUND, 'Inbound'),
        (OUTBOUND, 'Outbound'),
        (TRANSFER, 'Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    type = models.CharField(max_length=1, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
