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

    def _update_low_stock_flag(self):
        """Met à jour le flag d'alerte de stock faible."""
        self.is_low = self.quantity <= self.product.stock_threshold

    def _calculate_quantity_delta(self):
        """Calcule la différence de quantité par rapport à l'état précédent."""
        if self.id:
            cur_obj = Stock.objects.get(pk=self.id)
            return self.quantity - cur_obj.quantity
        return self.quantity

    def _create_stock_movement(self, delta):
        """Crée un mouvement de stock automatique basé sur le delta de quantité."""
        is_inbound = delta > 0
        movement_type = Movement.MovementType.INBOUND if is_inbound else Movement.MovementType.OUTBOUND
        
        movement = Movement(
            type=movement_type,
            quantity=delta,
            product=self.product,
            synced=True
        )

        if is_inbound:
            movement.to_location = self.location
        else:
            movement.from_location = self.location
            
        movement.save()

    def save(self, *args, **kwargs):
        # Mise à jour du flag d'alerte de stock faible
        self._update_low_stock_flag()

        # Gestion de la synchronisation avec les mouvements
        if self.synch:
            delta = self._calculate_quantity_delta()
            if delta != 0:
                self._create_stock_movement(delta)
        else:
            # Réactivation de la synchronisation si elle avait été désactivée
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

    def _update_origin_stock(self):
        """Met à jour le stock d'origine pour les mouvements OUTBOUND et TRANSFER."""
        from_stock, _ = Stock.objects.get_or_create(
            location=self.from_location,
            product=self.product,
            defaults={'quantity': 0, 'synch': False}
        )
        from_stock.quantity -= self.quantity
        from_stock.synch = False
        from_stock.save()

    def _update_destination_stock(self):
        """Met à jour le stock de destination pour les mouvements INBOUND et TRANSFER."""
        to_stock, _ = Stock.objects.get_or_create(
            location=self.to_location,
            product=self.product,
            defaults={'quantity': 0, 'synch': False}
        )
        to_stock.quantity += self.quantity
        to_stock.synch = False
        to_stock.save()

    def _should_update_origin_stock(self):
        """Détermine si le stock d'origine doit être mis à jour."""
        return self.type != Movement.MovementType.INBOUND

    def _should_update_destination_stock(self):
        """Détermine si le stock de destination doit être mis à jour."""
        return self.type != Movement.MovementType.OUTBOUND

    def save(self, *args, **kwargs):
        # Mise à jour des stocks uniquement si le mouvement n'est pas encore synchronisé
        # Les mouvements créés automatiquement par Stock ont synced=True par défaut
        if not self.synced:
            self.synced = True
            
            # Mise à jour du stock d'origine pour OUTBOUND et TRANSFER
            if self._should_update_origin_stock():
                self._update_origin_stock()

            # Mise à jour du stock de destination pour INBOUND et TRANSFER
            if self._should_update_destination_stock():
                self._update_destination_stock()

        super().save(*args, **kwargs)
