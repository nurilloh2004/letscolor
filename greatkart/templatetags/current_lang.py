from django import template

register = template.Library()

@register.simple_tag
def current_lang(request):
    url = str(request.path)
    parts = url.split("/")
    if parts[1] in ["ru", "uz", "en"]:
        return parts[1]
    else:
        return "ru"