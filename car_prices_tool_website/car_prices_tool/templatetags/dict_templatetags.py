from django.template.defaulttags import register


# Simple tag to retrieve value from dictionary based on key.
@register.simple_tag
def get_dict_key(dictionary, key):
    return dictionary.get(key)


# Simple tag to retrieve object from list with index from dictionary based on key.
@register.simple_tag
def get_dict_key_index(dictionary, key, index=0):
    return dictionary.get(key)[index]
