from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

def get_cheapest_price_from_market(keyword):
    print(f"🔍 Fiyat aranıyor: {keyword}")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://marketfiyati.org.tr/ara?q={keyword}"
        driver.get(url)
        time.sleep(5)

        product_cards = driver.find_elements(By.CSS_SELECTOR, "tubitak-product-summary")
        prices = []

        for card in product_cards:
            try:
                price_element = card.find_element(By.CSS_SELECTOR, "div.product-price span.fw-bold")
                price_text = price_element.text.strip()
                match = re.search(r"([\d.,]+)", price_text)
                if match:
                    price = float(match.group(1).replace(",", "."))
                    prices.append(price)
            except:
                continue

        driver.quit()

        if prices:
            return min(prices)
        else:
            return {"error": f"'{keyword}' için fiyat bulunamadı."}

    except Exception as e:
        driver.quit()
        return {"error": str(e)}

# Kullanıcıdan girdi al
if __name__ == "__main__":
    user_input = input("Malzeme adını girin: ")
    result = get_cheapest_price_from_market(user_input)

    if isinstance(result, dict):
        print("❌", result["error"])
    else:
        print(f"✅ En ucuz '{user_input}' fiyatı: {result} TL")

    
