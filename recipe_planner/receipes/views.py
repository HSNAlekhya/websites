from django.shortcuts import render, redirect
from .models import Recipe, MealPlan
from .forms import RecipeForm, MealPlanForm


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "receipes/recipe_list.html", {"recipes": recipes})


def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm()

    return render(request, "receipes/add_recipe.html", {"form": form})


def search(request):
    query = request.GET.get("q")

    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(title__icontains=query)

    return render(request, "receipes/search.html", {"recipes": recipes})


def meal_plan(request):
    meals = MealPlan.objects.all()
    return render(request, "receipes/meal_plan.html", {"meals": meals})


def add_meal(request):
    if request.method == "POST":
        form = MealPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("meal_plan")
    else:
        form = MealPlanForm()

    return render(request, "receipes/add_meal.html", {"form": form})

# Create your views here.
