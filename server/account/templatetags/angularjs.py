from django import template

register = template.Library()

@register.filter
def aj(value):
    return "{{%s}}" % str(value)
