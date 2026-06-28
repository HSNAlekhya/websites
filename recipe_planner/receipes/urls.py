from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("add/", views.add_recipe, name="add_recipe"),
    path("search/", views.search, name="search"),
    path("planner/", views.meal_plan, name="meal_plan"),
    path("planner/add/", views.add_meal, name="add_meal"),
]