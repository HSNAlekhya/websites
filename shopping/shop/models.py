from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    badge = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=50, blank=True)
    discount = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=50, blank=True)
    stock = models.PositiveIntegerField(default=0)
    material = models.CharField(max_length=100, blank=True)
    delivery_days = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name
