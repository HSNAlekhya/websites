from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import *
from .forms import *


def home(request):

    categories = Category.objects.all()

    products = Product.objects.filter(
        available=True
    ).order_by("-id")

    search = request.GET.get("q")

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {

        "categories": categories,

        "products": products,

        "search": search

    }

    return render(
        request,
        "home.html",
        context
    )


# ----------------------------
# REGISTER
# ----------------------------

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            Cart.objects.create(user=user)

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# ----------------------------
# LOGIN
# ----------------------------

def user_login(request):

    message = ""

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            password = form.cleaned_data["password"]

            user = authenticate(

                request,

                username=username,

                password=password

            )

            if user:

                login(request, user)

                return redirect("home")

            else:

                message = "Invalid Username or Password"

    else:

        form = LoginForm()

    return render(

        request,

        "login.html",

        {

            "form": form,

            "message": message

        }

    )


# ----------------------------
# LOGOUT
# ----------------------------

@login_required
def user_logout(request):
    logout(request)
    return render(request, "logout.html")


# ----------------------------
# CATEGORY PAGE
# ----------------------------

def category(request, id):

    category = get_object_or_404(

        Category,

        id=id

    )

    products = Product.objects.filter(

        category=category,

        available=True

    )

    return render(

        request,

        "category.html",

        {

            "category": category,

            "products": products

        }

    )


# ----------------------------
# PRODUCT DETAIL
# ----------------------------

def product_detail(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    return render(

        request,

        "product_detail.html",

        {

            "product": product

        }

    )

def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related("product")

    total = cart.total_price()

    return render(
        request,
        "cart.html",
        {
            "cart": cart,
            "items": items,
            "total": total,
        },
    )


# =====================================
# ADD TO CART
# =====================================

@login_required
def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")


# =====================================
# INCREASE QUANTITY
# =====================================

@login_required
def increase_quantity(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    if item.product.stock > item.quantity:
        item.quantity += 1
        item.save()

    return redirect("cart")


# =====================================
# DECREASE QUANTITY
# =====================================

@login_required
def decrease_quantity(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")


# =====================================
# REMOVE ITEM
# =====================================

@login_required
def remove(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")

# =====================================
# CHECKOUT
# =====================================

@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.all()

    if not items.exists():
        return redirect("cart")

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.user = request.user

            order.total = cart.total_price()

            order.save()

            for item in items:

                OrderItem.objects.create(

                    order=order,

                    product=item.product,

                    quantity=item.quantity,

                    price=item.product.price

                )

                product = item.product

                product.stock -= item.quantity

                product.save()

            items.delete()

            return redirect("orders")

    else:

        form = CheckoutForm()

    context = {

        "form": form,

        "cart": cart,

        "items": items,

        "total": cart.total_price()

    }

    return render(
        request,
        "checkout.html",
        context
    )


# =====================================
# MY ORDERS
# =====================================

@login_required
def orders(request):

    orders = Order.objects.filter(

        user=request.user

    ).order_by("-ordered_at")

    return render(

        request,

        "orders.html",

        {

            "orders": orders

        }

    )


# =====================================
# ORDER DETAILS
# =====================================

@login_required
def order_detail(request, id):

    order = get_object_or_404(

        Order,

        id=id,

        user=request.user

    )

    items = order.items.all()

    return render(

        request,

        "order_detail.html",

        {

            "order": order,

            "items": items

        }

    )


# =====================================
# PROFILE
# =====================================

@login_required
def profile(request):

    return render(

        request,

        "profile.html"

    )