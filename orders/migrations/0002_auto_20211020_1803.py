# Generated by Django 3.1 on 2021-10-20 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line_1',
            field=models.CharField(max_length=50, verbose_name='Address Line 1'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=50, verbose_name='Address Line 2'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=50, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=50, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ip',
            field=models.CharField(blank=True, max_length=20, verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_ordered',
            field=models.BooleanField(default=False, verbose_name='Is Ordered'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=100, verbose_name='Order Note'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, verbose_name='Order Number'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_total',
            field=models.FloatField(verbose_name='Order Total'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='Payment'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=50, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.FloatField(verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='Ordered'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='Payment'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product_price',
            field=models.FloatField(verbose_name='Product Price'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated At '),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation', verbose_name='Variations'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.CharField(max_length=100, verbose_name='Amount Paid'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=100, verbose_name='Payment Id'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=100, verbose_name='Payment Method'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(max_length=100, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
