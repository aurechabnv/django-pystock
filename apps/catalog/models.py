from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nom de catégorie")
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de produit")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Identifiant")
    price = models.FloatField(verbose_name="Prix")
    vat = models.FloatField(default=0.2, verbose_name="TVA")
    stock_threshold = models.IntegerField(verbose_name="Alerte de stock")
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name="Catégories")

    class Meta:
        verbose_name = "Produit"

    def __str__(self):
        return f"{self.name} [{self.sku}]"

    def save(self, *args, **kwargs):
        self.sku = self.sku.upper()
        super().save(*args, **kwargs)
