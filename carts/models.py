from django.db import models
from store.models import Product, Variation
from accounts.models import Account
from category.models import Category
from django.utils.translation import gettext_lazy as _


def generate_coupon_code():
    import random
    import string

    available_chars = string.ascii_letters + string.digits
    code = ""

    for i in range(8):
        index = random.randint(0, len(available_chars) - 1)
        code += available_chars[index]

    return code


def add_coupon(self):
    code = generate_coupon_code()
    coupons = Coupon.objects.filter(code=code)

    if not coupons.exists():
        coupon = Coupon(
            code=code,
            stock=self.stock,
            expires_in=self.expires_in
        )
        coupon.save()
        for category in self.category.all():
            print(category)
            coupon.category.add(category)
        coupon.save()
    else:
        add_coupon(self)


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, verbose_name=_('Cart Id'))
    date_added = models.DateField(auto_now_add=True, verbose_name=_('Date Added'))

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name=_('User'))
    ip = models.CharField(null=True, blank=True, max_length=20, verbose_name=_('IP'))
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variations = models.ManyToManyField(Variation, blank=True, verbose_name=_('Variations'))
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name=_('Cart'))

    reduced_price = models.FloatField(blank=True, default=0.0, verbose_name=_('Reduced Price'))

    quantity = models.IntegerField(verbose_name=_('Quantity'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    def total_price(self):
        if self.reduced_price != 0.0:
            return self.reduced_price * self.quantity
        else:
            return self.product.price * self.quantity

    def sub_total(self):
        return self.product.price * self.quantity

    def get_price(self):
        if self.reduced_price != 0.0:
            return self.reduced_price
        else:
            return self.product.price

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')


class Coupon(models.Model):
    code = models.CharField(max_length=8, blank=True, unique=True, verbose_name=_('Code'))
    stock = models.IntegerField(verbose_name=_('Stock'))
    expires_in = models.DateTimeField(verbose_name=_('Expires In'))
    category = models.ManyToManyField(Category, verbose_name=_('Category'))
    is_used = models.BooleanField(default=False, null=True, verbose_name=_('Is Used'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')


class CouponGroup(models.Model):
    count = models.PositiveIntegerField(verbose_name=_('Count'))
    stock = models.IntegerField(verbose_name=_('Stock'))
    expires_in = models.DateTimeField(verbose_name=_('Expires In'))
    category = models.ManyToManyField(Category, verbose_name=_('Category'))

    def save(self, *args, **kwargs):
        super(CouponGroup, self).save(*args, **kwargs)

        for _ in range(self.count):
            code = generate_coupon_code()
            coupons = Coupon.objects.filter(code=code)

            if not coupons.exists():
                coupon = Coupon(
                    code=code,
                    stock=self.stock,
                    expires_in=self.expires_in
                )
                coupon.save()
                coupon_group = CouponGroup.objects.get(count=self.count, stock=self.stock, expires_in=self.expires_in)
                coupon.category.add(*coupon_group.category.all())
                coupon.save()
            else:
                add_coupon(self)

    class Meta:
        verbose_name = _('Coupon Group')
        verbose_name_plural = _('Coupon Groups')
