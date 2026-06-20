from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('overview/', views.overview_view, name='overview'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('transactions/delete/<int:idx>/', views.delete_transaction, name='delete_transaction'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('action/<str:action>/', views.action_handler, name='action_handler'),
    path('monthly/', views.monthly_view, name='monthly'),
]
