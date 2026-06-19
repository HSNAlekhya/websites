from django.shortcuts import render, redirect
from shop.models import CartItem
from .models import Order, OrderItem


def checkout(request):
    items = CartItem.objects.select_related('product').all()
    if request.method == 'POST':
        total = sum(item.product.price * item.quantity for item in items)
        order = Order.objects.create(total=total)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
            )
        items.delete()
        return redirect('order_success')
    return render(request, 'orders/checkout.html', {'items': items})


def order_success(request):
    return render(request, 'orders/success.html')
