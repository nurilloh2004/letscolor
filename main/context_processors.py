from .models import Menu


def menu_footer(request):
    menu_footer = Menu.objects.all()
    return {"menu_footer": menu_footer}
