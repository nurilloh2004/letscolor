from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from .managers import CategoryManager
from django.urls import reverse


class Category(MPTTModel, TranslatableModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name=_('Parent'))

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_('Name'), null=True, blank=True),
    )
    slug = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Slug'))
    icon = models.ImageField(upload_to="icons/", blank=True, null=True, verbose_name=_('Icon'))

    objects = CategoryManager()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name = 'Category'
    #     verbose_name_plural = 'Categories'
    #
    # def __unicode__(self):
    #     return self.safe_translation_getter('name')
    #
    # #
    # # def get_url(self):
    # #      return reverse('products_by_category', args=[self.slug])
    # def save(self, *args, **kwargs):
    #     super(Category, self).save(*args, **kwargs)
    #     if not self.slug:
    #         self.slug = slugify(self.safe_translation_getter('name'), to_lower=True)
    #     super(Category, self).save(*args, **kwargs)



class Brand(TranslatableModel):
    translations = TranslatedFields(
        brand_name = models.CharField(max_length=50, unique=True, verbose_name=_('Brand Name')),
        description = models.TextField(max_length=255, blank=True, verbose_name=_('Description')),
    )
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    brand_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name=_('Brand Image'))


    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def get_url(self):
            return reverse('store_by_brands', args=[self.slug])

    def __str__(self):
        return self.brand_name
