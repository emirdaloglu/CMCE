from django.shortcuts import render
from django.http import JsonResponse
import json

from .malzeme_resim_scraper import get_recipe_data
from .en_ucuz_fiyat import get_cheapest_price_from_market
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def parse_ingredient(raw):
    parts = raw.split()
    if len(parts) < 3:
        return {"amount": 1, "unit": "", "name": raw}
    try:
        amount = float(parts[0].replace(",", "."))  # varsa ondalıklı
        unit = parts[1]
        name = " ".join(parts[2:])
    except:
        amount = 1
        unit = ""
        name = raw
    return {"amount": amount, "unit": unit, "name": name}

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

@csrf_exempt
def calculate_with_cost(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        meal_name = body.get('mealName')
        print("💡 İstek alındı:", meal_name)

        try:
            recipe_raw = get_recipe_data(meal_name)
            recipe = json.loads(recipe_raw) if isinstance(recipe_raw, str) else recipe_raw
            print("🧾 Gelen tarif verisi:", recipe)

            ingredients = [parse_ingredient(i) for i in recipe['ingredients']]
            image = recipe['image']
            description = recipe.get('description', '')

            total_cost = 0
            for ing in ingredients:
                price = get_cheapest_price_from_market(ing['name'])
                if isinstance(price, (int, float)):
                    ing['cost'] = price
                    total_cost += price
                    print("➕ Eklenen fiyat:", price, "Toplam:", total_cost)
                else:
                    ing['cost'] = None
                print("✅ JSON olarak frontend'e dönen veri:", {
                'meal': meal_name,
                'ingredients': ingredients,
                'total_cost': round(total_cost, 2),
                'image': image,
                'description': description,
            })

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