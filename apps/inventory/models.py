from django.contrib.auth import get_user_model
from django.db import models

from apps.catalog.models import Product


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


class Location(models.Model):
    class LocationType(models.TextChoices):
        SHOP = "SH", "Magasin"
        WAREHOUSE = "WH", "Entrepôt"

    class Meta:
        verbose_name = "site"

    type = models.CharField(max_length=2, choices=LocationType)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Société")
    name = models.CharField(max_length=100, verbose_name="Raison sociale")
    siret = models.CharField(max_length=14, blank=True, unique=True, null=True)
    address_line_1 = models.CharField(max_length=100, verbose_name="Adresse ligne 1")
    address_line_2 = models.CharField(max_length=100, blank=True, verbose_name="Adresse ligne 2")
    zip_code = models.CharField(max_length=10, verbose_name="Code postal")
    city = models.CharField(max_length=30, verbose_name="Ville")
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.name}{' [' + self.siret + ']' if self.siret else ''}"

    @property
    def full_address(self):
        return f"{self.address_line_1 + ', '}{self.address_line_2 + ', ' if self.address_line_2 else ''}{self.zip_code} {self.city}"


class Stock(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Site")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.IntegerField(verbose_name="Quantité")
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    synch = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.sku} - {self.location.company.name} - {self.location.name} ({self.location.LocationType(self.location.type).label})"

    def save(self, *args, **kwargs):
        # Create a stock movement in case of create/update if synch is enabled
        # Make sure to set the movement's attribute `synched` to True to prevent loop update Stock<>Movement
        if self.synch:
            if self.id:
                cur_obj = Stock.objects.get(pk=self.id)
                delta = self.quantity - cur_obj.quantity
            else:
                delta = self.quantity

            is_inbound = delta > 0
            movement_type = Movement.MovementType.INBOUND if is_inbound else Movement.MovementType.OUTBOUND
            movement = Movement(type=movement_type, quantity=delta, product=self.product, synced=True)

            if is_inbound:
                movement.to_location = self.location
            else:
                movement.from_location = self.location
            movement.save()
        else:
            # If synch has been bypassed by a movement direct update, re-enable it
            self.synch = True

        super().save(*args, **kwargs)


class Movement(models.Model):
    class MovementType(models.TextChoices):
        INBOUND = "I", "Entrée"
        OUTBOUND = "O", "Sortie"
        TRANSFER = "T", "Transfert"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+', verbose_name="Produit")
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name="Site d'origine", help_text="Nécessaire pour les sorties et transferts")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name="Site de destination", help_text="Nécessaire pour les entrées et transferts")
    type = models.CharField(max_length=1, choices=MovementType)
    quantity = models.IntegerField(verbose_name="Quantité")
    date = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)

    class Meta:
        verbose_name = "mouvement"

    def __str__(self):
        return f"{self.MovementType(self.type).label} du {self.date.strftime('%d-%m-%Y %H:%M')}"

    def save(self, *args, **kwargs):
        # Make sure to only update stocks if movement is not synched yet
        # Movement will be defaulted synched=True if it has been created from a stock update directly
        if not self.synced:
            self.synced = True
            # Get or create origin stock for OUTBOUND and TRANSFER
            if self.type != Movement.MovementType.INBOUND:
                from_stock, created = Stock.objects.get_or_create(
                    location=self.from_location,
                    product=self.product,
                    defaults={'quantity': 0, 'synch': False}
                )
                from_stock.quantity -= self.quantity
                from_stock.synch = False
                from_stock.save()

            # Get or create destination stock for INBOUND and TRANSFER
            if self.type != Movement.MovementType.OUTBOUND:
                to_stock, created = Stock.objects.get_or_create(
                    location=self.to_location,
                    product=self.product,
                    defaults={'quantity': 0, 'synch': False}
                )
                to_stock.quantity += self.quantity
                to_stock.synch = False
                to_stock.save()

        super().save(*args, **kwargs)
