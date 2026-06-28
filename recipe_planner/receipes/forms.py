from django import forms
from .models import Recipe, MealPlan


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"


class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = "__all__"