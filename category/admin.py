from django.contrib import admin
from .models import Category, Brand
from parler.admin import TranslatableAdmin
from mptt.admin import MPTTModelAdmin


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin, MPTTModelAdmin):
    mptt_level_indent = 50
    ordering = ['id']

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('name',)
        }


@admin.register(Brand)
class BrandAdmin(TranslatableAdmin):
    ordering = ['id']

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('brand_name',)
        }
