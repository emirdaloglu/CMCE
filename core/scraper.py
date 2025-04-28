# Birleştirilmiş scraper dosyası: malzeme_resim_ve_fiyat_scraper.py

import os
import time
import re
import requests
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

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

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/opt/homebrew/bin/chromedriver")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

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
            return {"error": "Hiçbir malzeme alanı bulunamadı."}

        full_text = element.get_attribute("innerText")
        ingredients = [line.strip() for line in full_text.split("\n") if line.strip()]

        try:
            image_element = driver.find_element("css selector", "meta[property='og:image']")
            image_url = image_element.get_attribute("content")
        except:
            image_url = None

        return {
            "meal": meal_name,
            "url": url,
            "image": image_url,
            "ingredients": ingredients
        }

    except Exception as e:
        return {"error": f"Hata oluştu: {e}"}
    finally:
        driver.quit()

def get_cheapest_price_from_market(product_name):
    print(f"🔍 Aranıyor: {product_name}")
    slug = slugify(product_name)
    url = f"https://marketfiyatlari.org/arama/{slug}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        price_elements = soup.select(".price")
        prices = []

        for el in price_elements:
            price_text = el.get_text(strip=True).replace("TL", "").replace(",", ".").strip()
            try:
                price_value = float(price_text)
                prices.append(price_value)
            except:
                continue

        if prices:
            return min(prices)
        return None

    except Exception as e:
        print(f"Hata: {e}")
        return None

# Test kodu
if __name__ == "__main__":
    meal = input("Yemek adı gir: ")
    data = get_recipe_data(meal)
    if "error" in data:
        print("❌", data["error"])
    else:
        print(f"\n✅ {data['meal']} Tarifi (Kaynak: {data['url']})")
        print(f"🖼️ Görsel: {data['image']}")
        for item in data['ingredients']:
            print(" -", item)

    if data.get("ingredients"):
        price = get_cheapest_price_from_market(data['ingredients'][0])
        print(f"\n✨ {data['ingredients'][0]} için en ucuz fiyat: {price} TL" if price else "Fiyat bulunamadı.")
