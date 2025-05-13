from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    vat = models.FloatField()
    stock_threshold = models.IntegerField()
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name
