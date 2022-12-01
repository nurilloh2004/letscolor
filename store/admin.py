from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails
from parler.admin import TranslatableAdmin, TranslatableTabularInline


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(TranslatableAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'brand', 'modified_date', 'is_available')
    #inlines = [ProductGalleryInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('product_name',)
        }

class VariationAdmin(TranslatableAdmin):
    list_display = ('product', 'variation_category', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
