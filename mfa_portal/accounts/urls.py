from django.urls import path
from . import views

urlpatterns = [

    path('',views.login_view,name='login'),

    path('otp/',views.otp_view,name='otp'),

    path('dashboard/',views.dashboard,name='dashboard'),

]