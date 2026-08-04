from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('home/',views.home,name='home'),
    path('search/', views.search_products, name='search_products'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup_view, name='signup_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('order-confirmed/', views.order_confirmed, name='order_confirmed'),
]
