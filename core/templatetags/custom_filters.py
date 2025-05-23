from django import template

register = template.Library()

@register.filter
def before_at(value):
    return value.split('@')[0] if '@' in value else value

@register.filter
def get_url(recipes, meal_name):
    for recipe in recipes:
        if recipe.name == meal_name:
            return recipe.url
    return ''