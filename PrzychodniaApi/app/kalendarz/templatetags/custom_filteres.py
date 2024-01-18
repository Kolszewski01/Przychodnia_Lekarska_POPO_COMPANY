from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@register.filter
def replace_colon(value, new_value='-'):
    return value.replace(":", new_value)