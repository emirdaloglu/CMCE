import os
import time
import re
import requests
import tempfile
import redis
import json
import urllib.parse
from datetime import datetime
from django.core.files import File
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .models import Recipe, Ingredient

# Redis connection
redis_client = redis.Redis(host='cmce-redis-1', port=6379, db=0)

def slugify(turkish_text):
    mapping = {
        "ç": "c", "Ç": "c",
        "ğ": "g", "Ğ": "g",
        "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o",
        "ş": "s", "Ş": "s",
        "ü": "u", "Ü": "u"
    }
    for turkish, ascii_char in mapping.items():
        turkish_text = turkish_text.replace(turkish, ascii_char)
    turkish_text = turkish_text.lower()
    turkish_text = re.sub(r'[^a-z0-9\s-]', '', turkish_text)
    turkish_text = turkish_text.replace(" ", "-")
    return turkish_text.strip("-")

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def save_recipe_image(recipe, image_url):
    if not image_url:
        return
    
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=True)
            temp_file.write(response.content)
            temp_file.flush()
            
            # Save the image to the recipe
            recipe.image.save(f"{slugify(recipe.name)}.jpg", File(temp_file), save=True)
            temp_file.close()
    except Exception as e:
        print(f"Error saving image: {e}")

def create_recipe_from_data(meal_name, user=None):
    cached = redis_client.get(f"recipe:{meal_name}")
    if cached:
        print(f"📦 Found in cache: {meal_name}")
        data = json.loads(cached)
    else:
        data = get_recipe_data(meal_name)
        if "error" in data:
            return None

    # Create or update recipe
    recipe, created = Recipe.objects.get_or_create(
        name=meal_name,
        defaults={
            'image_url': data.get('image'),
            'user': user
        }
    )

    if not created:
        recipe.image_url = data.get('image')
        recipe.save()

    # Save image if we have a URL
    if data.get('image') and not recipe.image:
        save_recipe_image(recipe, data.get('image'))

    # Update ingredients
    for ingredient_name in data.get('ingredients', []):
        ingredient, created = Ingredient.objects.get_or_create(
            recipe=recipe,
            name=ingredient_name
        )
        if created or not ingredient.current_price:
            price = get_cheapest_price_from_market(ingredient_name, meal_name)
            if price:
                ingredient.current_price = price
                ingredient.last_price_update = datetime.now()
                ingredient.save()

    return recipe

def get_recipe_data(meal_name):
    slug = slugify(meal_name)
    url = f"https://www.nefisyemektarifleri.com/{slug}/"
    print(f"🔗 URL: {url}")

    driver = get_driver()

    try:
        driver.get(url)
        time.sleep(3)

        possible_selectors = [
            ".recipe-materials",
            ".recipe-materials-inner",
            ".recipe-material-content",
            ".recipe-content"
        ]
        element = None
        for selector in possible_selectors:
            try:
                element = driver.find_element("css selector", selector)
                if element and element.get_attribute("innerText").strip():
                    break
            except:
                continue

        if not element:
            return {"error": "No ingredient area found."}

        full_text = element.get_attribute("innerText")
        ingredients = [line.strip() for line in full_text.split("\n") if line.strip()]

        try:
            image_element = driver.find_element("css selector", "meta[property='og:image']")
            image_url = image_element.get_attribute("content")
        except:
            image_url = None

        result = {
            "meal": meal_name,
            "url": url,
            "image": image_url,
            "ingredients": ingredients
        }

        redis_client.set(f"recipe:{meal_name}", json.dumps(result), ex=60*60*24)
        return result

    except Exception as e:
        return {"error": f"Error occurred: {e}"}
    finally:
        driver.quit()

def update_ingredient_prices():
    """Update prices for all ingredients that haven't been updated in the last 6 hours"""
    six_hours_ago = datetime.now() - timedelta(hours=6)
    ingredients = Ingredient.objects.filter(
        models.Q(last_price_update__isnull=True) |
        models.Q(last_price_update__lt=six_hours_ago)
    )

    for ingredient in ingredients:
        price = get_cheapest_price_from_market(ingredient.name, ingredient.recipe.name)
        if price:
            ingredient.current_price = price
            ingredient.last_price_update = datetime.now()
            ingredient.save()

def get_cheapest_price_from_market(product_name, meal_name=None):
    cached = redis_client.get(f"price:{product_name}")
    if cached:
        print(f"📦 Found in cache (price): {product_name}")
        return float(cached)

    print(f"🔍 Searching: {product_name}")
    query = urllib.parse.quote(product_name)
    url = f"https://marketfiyati.org.tr/ara?q={query}"

    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(3)  # Wait for JS to load
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price_elements = soup.select("span.fw-bold.caption-16.secondary-700")
        if not price_elements:
            print(f"[DEBUG] No price elements found for {product_name}. HTML snippet:\n{driver.page_source[:1000]}")
        for el in price_elements:
            price_text = el.get_text(strip=True).replace("₺", "").replace(",", ".").strip()
            try:
                price_value = float(price_text)
                redis_client.set(f"price:{product_name}", price_value, ex=60*60*6)
                return price_value
            except Exception:
                continue
    except Exception as e:
        print(f"⚠️ Selenium scraper error: {e}")
    finally:
        driver.quit()

    return None