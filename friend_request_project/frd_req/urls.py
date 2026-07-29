from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("send/<int:id>/", views.send_request, name="send"),
    path("requests/", views.requests, name="requests"),
    path("accept/<int:id>/", views.accept_request, name="accept"),
    path("delete/<int:id>/", views.delete_request, name="delete"),
    path("remove/<int:id>/", views.remove_friend, name="remove"),
]