INGREDIENT_MAPPING = {
    "nişasta": "buğday nişastası",
    "yumurta beyazı": "yumurta",
    "yumurta sarısı": "yumurta",
    "limon suyu": "limon",
    "çiğ badem": "badem",
    "şeker": "toz şeker",
    "tuz": "iyotlu tuz",
    "sıcak su": "su",
    "ılık su": "su",
    "sıvı yağ": "ay çiçek yağı",
    # Add more as needed
}

def map_ingredient_name(ingredient):
    ing = ingredient.lower()
    if ing == "sarımsaklı yoğurt":
        return ["sarımsak", "yoğurt"]
    return INGREDIENT_MAPPING.get(ing, ingredient) 