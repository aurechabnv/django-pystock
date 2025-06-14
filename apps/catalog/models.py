from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nom de catégorie")
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "catégorie"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de produit")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Identifiant")
    price = models.FloatField(verbose_name="Prix", default=0)
    vat = models.FloatField(default=0.2, verbose_name="TVA")
    stock_threshold = models.IntegerField(verbose_name="Alerte de stock", default=0)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name="Catégories")
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "produit"

    def __str__(self):
        return f"{self.name} [{self.sku}]"

    def get_categories(self):
        return ", ".join([c.name for c in self.categories.all()])

    def save(self, *args, **kwargs):
        self.sku = self.sku.upper()
        super().save(*args, **kwargs)
