from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.booking_calendar,
        name='booking'
    ),

    path(
        'success/',
        views.success,
        name='success'
    ),
]