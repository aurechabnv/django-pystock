from django.db import models

from apps.catalog.models import Product


class Company(models.Model):
    name = models.CharField(max_length=100)
    siret = models.CharField(max_length=14)
    phone = models.CharField(max_length=11, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} [{self.siret}]"


class Location(models.Model):
    class LocationType(models.TextChoices):
        SHOP = "SH", "Shop"
        WAREHOUSE = "WH", "Warehouse"

    type = models.CharField(max_length=2, choices=LocationType)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    siret = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type.label})"


class Stock(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x '{self.product.name}' ({self.location.name})"


class Movement(models.Model):
    class MovementType(models.TextChoices):
        INBOUND = "I", "Inbound"
        OUTBOUND = "O", "Outbound"
        TRANSFER = "T", "Transfer"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    type = models.CharField(max_length=1, choices=MovementType)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        location = ""
        if self.from_location:
            location += f"from '{self.from_location.name}'"
        if self.to_location:
            if location:
                location += " "
            location += f"to '{self.to_location.name}'"
        return f"{self.quantity}x '{self.product.name}' {location} ({self.type.label})"

    def save(self, *args, **kwargs):
        # Get origin location for OUTBOUND and TRANSFER
        if self.type != Movement.MovementType.INBOUND:
            from_stock = Stock.objects.get(location=self.from_location, product=self.product)
        else:
            from_stock = None

        # Get destination location for INBOUND and TRANSFER
        if self.type != Movement.MovementType.OUTBOUND:
            to_stock = Stock.objects.get(location=self.to_location, product=self.product)
        else:
            to_stock = None

        # Update stocks accordingly
        if from_stock:
            from_stock.quantity -= self.quantity
            from_stock.save()
        if to_stock:
            to_stock.quantity += self.quantity
            to_stock.save()

        super().save(*args, **kwargs)
