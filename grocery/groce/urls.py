from django.urls import path
from . import views

urlpatterns=[

path('',views.user_login,name='login'),

path('category/<int:id>/',views.category,name='category'),

path('product/<int:id>/',views.product_detail,name='product_detail'),

path('cart/',views.cart,name='cart'),

path('add/<int:id>/',views.add_to_cart,name='add_to_cart'),

path("increase/<int:id>/", views.increase_quantity, name="increase_quantity"),

path("decrease/<int:id>/", views.decrease_quantity, name="decrease_quantity"),

path('remove/<int:id>/',views.remove,name='remove'),

path('checkout/',views.checkout,name='checkout'),

path('register/',views.register,name='register'),

path('logout/',views.user_logout,name='logout'),

path('home/',views.home,name='home'),

path('orders/',views.orders,name='orders'),

path("orders/<int:id>/", views.order_detail, name="order_detail"),

path("profile/", views.profile, name="profile"),

]