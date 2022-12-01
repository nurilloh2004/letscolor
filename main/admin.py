from django.contrib import admin
from .models import Partners, Menu, About, Banners
from parler.admin import TranslatableAdmin


# Register your models here.

@admin.register(Menu)
class MenuAdmin(TranslatableAdmin):
    pass


admin.site.register(Partners)
admin.site.register(Banners)


@admin.register(About)
class AboutAdmin(TranslatableAdmin):
    pass
