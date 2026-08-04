from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from .models import Category, Product


def _product_image_url(category_slug, product_name, index):
    name_lower = (product_name or '').lower()
    category_slug = (category_slug or '').replace('-', ' ').strip()

    if 'kurti' in name_lower:
        asset = 'kurti.svg'
    elif 'lehenga' in name_lower:
        asset = 'lehenga.svg'
    elif 'saree' in name_lower:
        asset = 'saree.svg'
    elif 'skirt' in name_lower:
        asset = 'skirt.svg'
    elif 'dress' in name_lower or 'gown' in name_lower:
        asset = 'dress.svg'
    elif 'jacket' in name_lower:
        asset = 'jacket.svg'
    elif 'hoodie' in name_lower:
        asset = 'hoodie.svg'
    elif 'coat' in name_lower or 'blazer' in name_lower:
        asset = 'coat.svg'
    elif 'bag' in name_lower or 'wallet' in name_lower or 'necklace' in name_lower or 'watch' in name_lower or 'sunglasses' in name_lower:
        asset = 'bag.svg'
    elif 'shirt' in name_lower:
        asset = 'shirt.svg'
    elif 'trouser' in name_lower or 'trousers' in name_lower or 'jeans' in name_lower:
        asset = 'trousers.svg'
    elif 'polo' in name_lower or 'top' in name_lower or 'tee' in name_lower:
        asset = 'top.svg'
    elif 'shorts' in name_lower or 'romper' in name_lower or 'frock' in name_lower or 'cap' in name_lower:
        asset = 'kids.svg'
    elif category_slug.lower().startswith('womens'):
        asset = 'womens.svg'
    elif category_slug.lower().startswith('mens'):
        asset = 'mens.svg'
    elif category_slug.lower().startswith('accessories'):
        asset = 'accessories.svg'
    elif category_slug.lower().startswith('kids'):
        asset = 'kids.svg'
    else:
        asset = 'default.svg'

    return f"/static/shop/images/{asset}"


def _ensure_product_image(product, category_slug=None):
    if product.image_url:
        return product  # already has a real image (e.g. Pexels URL) — don't overwrite it

    category_slug = category_slug or getattr(product.category, 'slug', 'stylehub')
    product.image_url = _product_image_url(category_slug, product.name, product.id)
    product.save(update_fields=['image_url'])
    return product


def _seed_products_for_category(category):
    existing_products = list(category.products.order_by('id'))
    target_count = 20

    base_names = {
        'womens-wear': ['Floral Kurti', 'Party Dress', 'Casual Top', 'Elegant Skirt', 'Festive Set', 'Printed Saree', 'Denim Jacket', 'Office Wear', 'Ethnic Co-ord', 'Weekend Tunic'],
        'mens-wear': ['Classic Shirt', 'Casual Jacket', 'Formal Trousers', 'Smart Polo', 'Weekend Hoodie', 'Denim Shirt', 'Slim Fit Jeans', 'Winter Coat', 'Sports Tee', 'Formal Blazer'],
        'accessories': ['Statement Bag', 'Sunglasses', 'Layered Necklace', 'Leather Wallet', 'Silk Scarf', 'Mini Crossbody', 'Watch', 'Bracelet Set', 'Hair Clip', 'Travel Tote'],
        'kids-wear': ['Play Set', 'Printed Tee', 'Soft Jacket', 'Mini Dress', 'Comfy Shorts', 'Cotton Romper', 'Star Hoodie', 'Party Frock', 'Jogger Set', 'Sunny Cap'],
    }

    names = base_names.get(category.slug, ['StyleHub Essential', 'Colorful Pick', 'Smart Choice', 'Fresh Style', 'Everyday Favorite'])

    if len(existing_products) < target_count:
        for index in range(len(existing_products) + 1, target_count + 1):
            product_name = f"{names[(index - 1) % len(names)]} {index}"
            Product.objects.create(
                name=product_name,
                slug=f"{slugify(category.slug)}-{index}",
                category=category,
                price=999 + index * 99,
                description=f"Trendy {category.name.lower()} pick for everyday style.",
                image_url=_product_image_url(category.slug, product_name, index),
                badge='New' if index <= 3 else 'Bestseller',
                is_featured=index <= 4,
                brand='StyleHub',
                colour=['Pink', 'Blue', 'Black', 'Green', 'Mustard'][(index - 1) % 5],
                discount=10 + (index % 4) * 5,
                size=['S', 'M', 'L', 'XL', 'Free Size'][(index - 1) % 5],
                stock=10 + index,
                material='Cotton',
                delivery_days=3,
            )

    for index, product in enumerate(category.products.order_by('id')[:target_count], start=1):
        product_name = f"{names[(index - 1) % len(names)]} {index}"
        product.name = product.name or product_name
        product.description = product.description or f"Trendy {category.name.lower()} pick for everyday style."
        product.save(update_fields=['name', 'description'])


def _ensure_category(slug):
    category, created = Category.objects.get_or_create(
        slug=slug,
        defaults={
            'name': slug.replace('-', ' ').title(),
            'description': 'Fresh picks for this collection.'
        }
    )
    _seed_products_for_category(category)
    return category


def home(request):
    categories = Category.objects.all()
    featured_products = list(Product.objects.filter(is_featured=True)[:8])
    for product in featured_products:
        _ensure_product_image(product, category_slug=product.category.slug if product.category else 'stylehub')
    return render(request, 'shop/home.html', {'categories': categories, 'featured_products': featured_products})


def category_products(request, slug):
    category = _ensure_category(slug)
    products = list(category.products.all()[:20])
    for product in products:
        _ensure_product_image(product, category_slug=category.slug)
    return render(request, 'shop/category.html', {'category': category, 'products': products})


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    _ensure_product_image(product, category_slug=category_slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def search_products(request):
    query = request.GET.get('q', '')
    products = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query)
        )[:20]
    return render(request, 'shop/search_results.html', {'query': query, 'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.session.get('wishlist', [])
    if str(product.id) not in wishlist:
        wishlist.append(str(product.id))
    request.session['wishlist'] = wishlist
    return redirect('wishlist')


def wishlist(request):
    wishlist_ids = request.session.get('wishlist', [])
    wishlist_items = Product.objects.filter(id__in=wishlist_ids)
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})


def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'shop/logout.html')


def order_confirmed(request):
    if 'cart' in request.session:
        request.session['cart'] = {}
    return render(request, 'shop/order_confirmed.html')