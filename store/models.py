from django.db import models
from parler.managers import TranslatableQuerySet, TranslatableManager

from category.models import Category, Brand
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


# Create your models here.

class Product(TranslatableModel):
    CURRENCY = [
        ("uzs", "UZS"),
        ("usd", "USD")
    ]
    translations = TranslatedFields(
        product_name=models.CharField(max_length=200, verbose_name=_(
            'Product Name'), null=True, blank=True),
        short_description=models.TextField(
            max_length=255, blank=True, verbose_name=_('Short Description'), null=True),
        description=models.TextField(
            max_length=1500, blank=True, verbose_name=_('Description'), null=True),
    )
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name=_('Slug'), null=True, blank=True)
    old_price = models.FloatField(
        default=0, verbose_name=_('Old Price'), null=True, blank=True)
    original_price = models.FloatField(
        verbose_name=_('Price'), null=True, blank=True)
    currency = models.CharField(
        max_length=50, choices=CURRENCY, default="usd", null=True, blank=True)
    images = models.ImageField(
        upload_to='photos/products', verbose_name=_('Images'), null=True, blank=True)
    image_change = models.ImageField(
        upload_to='photos/products', blank=True, null=True, verbose_name=_('Image Change'))
    stock = models.IntegerField(verbose_name=_('Stock'), null=True, blank=True)
    is_available = models.BooleanField(
        default=True, verbose_name=_('Is Available'), null=True, blank=True)
    confirmation = models.BooleanField(
        default=False, verbose_name=_('In Hand'), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_(
        'Category'), null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Brand'))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created Date'))
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=_('Modified Date'))

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.safe_translation_getter("product_name", any_language=True) or ""

    def __unicode__(self):
        return self.safe_translation_getter("product_name", any_language=True)

    def averageReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def save(self, *args, **kwargs):
        from random import randint
        num = randint(0, 9)
        while Product.objects.filter(slug=self.slug).exists():
            self.slug = self.slug + str(num)

        return super(Product, self).save(*args, **kwargs)

    @property
    def price(self):
        if self.currency == "usd":
            return self.usd2uzs(self.original_price)
        return self.original_price

    @staticmethod
    def usd2uzs(usd):
        from dynamic_preferences.registries import global_preferences_registry
        gpm = global_preferences_registry.manager()
        if not usd:
            return " "
        result = int(usd * gpm["currency__usd"])
        rem = result % 1000
        if rem >= 500:
            result = ((result // 1000) * 1000) + ((rem // 100) + 1) * 100
        else:
            result = ((result // 1000) * 1000) + (rem // 100) * 100
        return result

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class VariationQuerySet(TranslatableQuerySet):
    def as_manager(cls):
        manager = VariationManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class VariationManager(TranslatableManager):
    _queryset_class = VariationQuerySet

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(TranslatableModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice, verbose_name=_('Variation Category'))
    translations = TranslatedFields(
        variation_value=models.CharField(
            max_length=100, verbose_name=_('Variation Value')),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_date = models.DateTimeField(
        auto_now=True, verbose_name=_('Created Date'))

    objects = VariationManager()

    class Meta:
        verbose_name = _('Variation')
        verbose_name_plural = _('Variations')

    def __str__(self):
        return str(self.variation_value)


class ReviewRating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=_('User'))
    subject = models.CharField(
        max_length=100, blank=True, verbose_name=_('Subject'))
    review = models.TextField(
        max_length=500, blank=True, verbose_name=_('Review'))
    rating = models.FloatField(verbose_name=_('Rating'))
    ip = models.CharField(max_length=20, blank=True, verbose_name=_('IP'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _('Review Rating')
        verbose_name_plural = _('Review Ratings')


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, verbose_name=_('Product'))
    image = models.ImageField(
        upload_to='store/products', max_length=255, verbose_name=_('Image'))

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = _('Product Gallery')
        verbose_name_plural = _('Product Gallery')
