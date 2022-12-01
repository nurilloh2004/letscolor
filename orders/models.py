from django.db import models
from accounts.models import Account
from store.models import Product, Variation
from django.utils.translation import ugettext_lazy as _



class Payment(models.Model):
    ip = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    payment_id = models.CharField(max_length=100, verbose_name=_('Payment Id'))
    payment_method = models.CharField(max_length=100, verbose_name=_('Payment Method'))
    amount_paid = models.CharField(max_length=100, verbose_name=_('Amount Paid'))  # this is the total amount paid
    status = models.CharField(max_length=100, verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('User'))
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Payment'))
    order_number = models.CharField(max_length=20, verbose_name=_('Order Number'))
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    phone = models.CharField(max_length=15, verbose_name=_('Phone'))
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name=_('Email'))
    address_line_1 = models.CharField(max_length=50, verbose_name=_('Address Line 1'))
    address_line_2 = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Address Line 2'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Country'))
    state = models.CharField(max_length=50, blank=True, null=True,  verbose_name=_('State'))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('City'))
    order_note = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Order Note'))
    order_total = models.FloatField(verbose_name=_('Order Total'))
    tax = models.FloatField(verbose_name=_('Tax'))
    status = models.CharField(max_length=10, choices=STATUS, default='New', verbose_name=_('Status'))
    ip = models.CharField(null=True, blank=True, max_length=20, verbose_name=_('IP'))
    is_ordered = models.BooleanField(default=False, verbose_name=_('Is Ordered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1 or ""} {self.address_line_2 or ""}'

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
    
    @property
    def total_price(self):
        total = 0.0
        for item in self.items.all():
            total += item.quantity * item.product_price
        return total


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'), related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variations = models.ManyToManyField(Variation, blank=True, verbose_name=_('Variations'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    product_price = models.FloatField(verbose_name=_('Product Price'))
    ordered = models.BooleanField(default=False, verbose_name=_('Ordered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At '))

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = _('OrderProduct')
        verbose_name_plural = _('OrderProducts')


class BotAdmin(models.Model):
    user_id = models.CharField(max_length=12)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.user_id, self.is_active)