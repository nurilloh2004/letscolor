from django import template

register = template.Library()

@register.simple_tag
def reverse_lang(request, lang):
    url = str(request.path)
    parts = url.split("/")
    parts[1] = lang
    new_url = "/".join(parts)
    return new_url