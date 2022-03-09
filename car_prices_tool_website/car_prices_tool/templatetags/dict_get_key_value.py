from django.template.defaulttags import register


@register.simple_tag
def get_dict_key(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def get_dict_key_index(dictionary, key, index=0):
    return dictionary.get(key)[index]
