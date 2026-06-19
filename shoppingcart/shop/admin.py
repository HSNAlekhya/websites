from django.contrib import admin
from .models import Product, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'added_at')
