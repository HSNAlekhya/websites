from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    name=models.CharField(max_length=200)

    image=models.ImageField(upload_to='products/')

    price=models.DecimalField(max_digits=8,decimal_places=2)

    description=models.TextField()

    stock=models.PositiveIntegerField(default=1)

    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.subtotal()
        return total

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

        order = models.ForeignKey(
            Order,
            on_delete=models.CASCADE,
            related_name="items"
        )

        product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE
        )

        quantity = models.PositiveIntegerField(default=1)

        price = models.DecimalField(max_digits=10, decimal_places=2)

        def subtotal(self):
            return self.price * self.quantity

        def __str__(self):
            return self.product.name

    # Create your models here.
