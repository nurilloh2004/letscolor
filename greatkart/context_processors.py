from django.conf import settings


def current_lang_path(request):
    context = {
        "languages": settings.PARLER_LANGUAGES[None]
    }
    return context
