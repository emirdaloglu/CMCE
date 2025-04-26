from django import template

register = template.Library()

@register.filter
def before_at(value):
    return value.split('@')[0] if '@' in value else value