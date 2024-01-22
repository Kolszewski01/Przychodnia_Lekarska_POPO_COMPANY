from django import template

register = template.Library()

@register.filter
def get_item(list, index):
    if 0 <= index < len(list):
        return list[index]
    else:
        return None



@register.filter
def replace_colon(value, new_value='-'):
    return value.replace(":", new_value)