from decimal import Decimal

from shop.models import Product, CartItem

# Create sample products
p1, _ = Product.objects.get_or_create(
    name='Widget',
    defaults={'price': Decimal('9.99'), 'description': 'Sample widget'}
)

p2, _ = Product.objects.get_or_create(
    name='Gadget',
    defaults={'price': Decimal('19.99'), 'description': 'Sample gadget'}
)

p3, _ = Product.objects.get_or_create(
    name='Thing',
    defaults={'price': Decimal('4.50'), 'description': 'Sample thing'}
)

# Add items to cart
CartItem.objects.update_or_create(product=p1, defaults={'quantity': 2})
CartItem.objects.update_or_create(product=p2, defaults={'quantity': 1})

print('Seeded products and cart items: Widget (2), Gadget (1), Thing (0)')
