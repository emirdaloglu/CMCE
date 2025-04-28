from django.shortcuts import render
from django.http import JsonResponse
import json

from core.scraper import get_recipe_data, get_cheapest_price_from_market
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import MealHistory
from .models import Favorite






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
        amount = float(parts[0].replace(",", "."))  # varsa ondalıklı
        unit = parts[1]
        name = " ".join(parts[2:])
    except:
        amount = 1
        unit = ""
        name = raw

    # 🔍 Anahtar kelime sadeleştirme (son kelimeyi al)
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

            # 📝 Kullanıcı giriş yapmışsa geçmişe kaydet
            if request.user.is_authenticated:
                MealHistory.objects.create(
                    user=request.user,
                    meal_name=meal_name,
                    total_cost=round(total_cost, 2)
                )

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

@csrf_exempt
def add_to_favorites(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        meal_name = body.get('mealName')
        total_cost = body.get('totalCost')

        if request.user.is_authenticated:
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
                pass  # Zaten yoksa hata verme
        return redirect('/favorites/')
    else:
        return redirect('/')