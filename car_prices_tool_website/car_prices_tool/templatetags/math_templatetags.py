from django.template.defaulttags import register


# Simple tag to easily multiply two values.
@register.simple_tag
def multiply(value_1, value_2):
    return value_1 * value_2
