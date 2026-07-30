from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_document, name="upload"),
    path("update/<int:id>/", views.update_document, name="update"),
    path("delete/<int:id>/", views.delete_document, name="delete"),
]