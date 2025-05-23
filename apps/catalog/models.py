from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    vat = models.FloatField(default=0.2)
    stock_threshold = models.IntegerField()
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name
