from django.shortcuts import render
from django.http import JsonResponse
import json

from core.scraper import get_recipe_data, get_cheapest_price_from_market
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import MealHistory, Recipe, Ingredient
from .models import Favorite
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect




def chatbot_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/chatbot/')
    return render(request, 'chatbot.html')


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if "@" not in email:
            return render(request, 'register.html', {'error': 'Geçerli bir e-mail adresi giriniz.'})

        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Bu e-posta zaten kayıtlı.'})

        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Kullanıcı adı veya şifre hatalı.'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def parse_ingredient(raw):
    parts = raw.split()
    if len(parts) < 3:
        return {"amount": 1, "unit": "", "name": raw}
    try:
        amount = float(parts[0].replace(",", "."))
        unit = parts[1]
        name = " ".join(parts[2:])
    except:
        amount = 1
        unit = ""
        name = raw

    name = name.split()[-1]
    return {"amount": amount, "unit": unit, "name": name}


def index(request):
    return render(request, 'index.html')


def add_recipe(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'add_recipe.html')


def corbalar(request):
    return render(request, 'corbalar.html')


def et_yemekleri(request):
    return render(request, 'et_yemekleri.html')


def favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).order_by('-date_added')
        return render(request, 'favorites.html', {'favorites': favorites})
    else:
        return redirect('/login/')


def history(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    histories = MealHistory.objects.filter(user=request.user).order_by('-date')
    return render(request, 'history.html', {'histories': histories})


@csrf_exempt
def calculate_with_cost(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Giriş yapmanız gerekiyor.'}, status=401)

        body = json.loads(request.body)
        meal_name = body.get('mealName')
        print("💡 İstek alındı:", meal_name)

        try:
            # Try to get the recipe from the database
            try:
                recipe = Recipe.objects.get(name__iexact=meal_name)
            except Recipe.DoesNotExist:
                return JsonResponse({'error': f"'{meal_name}' tarifi veritabanında bulunamadı. Lütfen başka bir yemek adı deneyin."}, status=404)

            ingredients_qs = Ingredient.objects.filter(recipe=recipe)
            if not ingredients_qs.exists():
                return JsonResponse({'error': f"'{meal_name}' için veritabanında malzeme bulunamadı."}, status=404)

            ingredients = []
            total_cost = 0
            for ing in ingredients_qs:
                price = get_cheapest_price_from_market(ing.name, meal_name)
                ingredient_data = {
                    'amount': ing.quantity or 1,
                    'unit': ing.unit or '',
                    'name': ing.name,
                    'cost': price if isinstance(price, (int, float)) else None
                }
                if ingredient_data['cost'] is not None:
                    total_cost += ingredient_data['cost']
                ingredients.append(ingredient_data)

            # Save to history
            MealHistory.objects.create(
                user=request.user,
                meal_name=meal_name,
                total_cost=round(total_cost, 2)
            )

            return JsonResponse({
                'meal': meal_name,
                'ingredients': ingredients,
                'total_cost': round(total_cost, 2),
                'image': recipe.image.url if recipe.image else recipe.image_url or '',
                'description': '',
            })

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})


@csrf_exempt
def add_to_favorites(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        meal_name = body.get('mealName')
        total_cost = body.get('totalCost')

        if request.user.is_authenticated:
            already_exists = Favorite.objects.filter(user=request.user, meal_name=meal_name).exists()
            if already_exists:
                return JsonResponse({'already': True})

            Favorite.objects.create(
                user=request.user,
                meal_name=meal_name,
                total_cost=total_cost
            )
            return JsonResponse({'message': 'Favorilere eklendi.'})
        else:
            return JsonResponse({'error': 'Giriş yapmanız gerekiyor.'}, status=401)

    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)


@csrf_exempt
def remove_favorite(request):
    if request.method == 'POST':
        favorite_id = request.POST.get('favorite_id')
        if favorite_id:
            try:
                fav = Favorite.objects.get(id=favorite_id, user=request.user)
                fav.delete()
            except Favorite.DoesNotExist:
                pass
        return redirect('/favorites/')
    else:
        return redirect('/')


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if not user_message:
            return JsonResponse({'message': 'Mesaj boş olamaz.'}, status=400)

        try:
            import requests
            ollama_response = requests.post(
                'http://ollama:11434/api/generate',
                json={
                    "model": "smollm2:360m",
                    "prompt": user_message
                },
                timeout=30,
                stream=True
            )
            ollama_response.raise_for_status()

            full_response = ''
            for line in ollama_response.iter_lines():
                if line:
                    part = line.decode('utf-8')
                    if part.startswith('{') and part.endswith('}'):
                        part_json = json.loads(part)
                        full_response += part_json.get('response', '')

            return JsonResponse({'message': full_response})

        except requests.RequestException as e:
            return JsonResponse({'message': f'Hata: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Sadece POST metoduna izin verilir.'}, status=405)


def tarifler(request):
    recipes = Recipe.objects.all()
    return render(request, 'tarifler.html', {'recipes': recipes})