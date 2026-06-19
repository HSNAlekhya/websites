from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('product_list')


def cart_view(request):
    items = CartItem.objects.select_related('product').all()
    return render(request, 'shop/cart.html', {'items': items})
