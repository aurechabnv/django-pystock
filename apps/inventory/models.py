from django.db import models

from apps.catalog.models import Product
from apps.management.models import Location


class Stock(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Site")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.IntegerField(verbose_name="Quantité", default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    synch = models.BooleanField(default=True)
    is_low = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.sku} - {self.location.company.name} - {self.location.name} ({self.location.LocationType(self.location.type).label})"

    def save(self, *args, **kwargs):
        # Update the stock `is_low` flag on save
        self.is_low = self.quantity <= self.product.stock_threshold

        # Create a stock movement in case of create/update if synch is enabled
        # Make sure to set the movement's attribute `synched` to True to prevent loop update Stock<>Movement
        if self.synch:
            if self.id:
                cur_obj = Stock.objects.get(pk=self.id)
                delta = self.quantity - cur_obj.quantity
            else:
                delta = self.quantity

            if delta != 0:
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
    quantity = models.IntegerField(verbose_name="Quantité", default=0)
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
