from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_asset, name='add_asset'),
    path('request/', views.request_asset, name='request_asset'),
    path('request/<int:asset_id>/', views.request_asset, name='request_asset_with_id'),
]