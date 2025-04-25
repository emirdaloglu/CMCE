from django.shortcuts import render
from django.http import JsonResponse
import json

from .malzeme_resim_scraper import get_recipe_data
from .en_ucuz_fiyat import get_cheapest_price_from_market
# Create your views here.


def index(request):
    return render(request, 'index.html')

def add_recipe(request):
    return render(request, 'add_recipe.html')

def corbalar(request):
    return render(request, 'corbalar.html')

def et_yemekleri(request):
    return render(request, 'et_yemekleri.html')

def favorites(request):
    return render(request, 'favorites.html')

def history(request):
    return render(request, 'history.html')

def calculate_with_cost(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        meal_name = body.get('mealName')

        try:
            recipe = get_recipe_data(meal_name)
            ingredients = recipe['ingredients']
            image = recipe['image']
            description = recipe['description']

            total_cost = 0
            for ing in ingredients:
                price = get_cheapest_price_from_market(ing['name'])
                ing['cost'] = price
                if price:
                    total_cost += price

            return JsonResponse({
                'meal': meal_name,
                'ingredients': ingredients,
                'total_cost': round(total_cost, 2),
                'image': image,
                'description': description,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})