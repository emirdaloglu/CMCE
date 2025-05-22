from django.contrib import admin
from .models import Recipe, Ingredient, MealHistory, Favorite

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(MealHistory)
admin.site.register(Favorite)
