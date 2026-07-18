from django.urls import path

from .views import (event_create, event_delete, event_detail, event_update,
                    home, login_view, logout_view, register_view)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('events/new/', event_create, name='event-create'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('events/<int:pk>/edit/', event_update, name='event-update'),
    path('events/<int:pk>/delete/', event_delete, name='event-delete'),
]
