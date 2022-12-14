# Generated by Django 3.1 on 2021-10-20 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211020_2146'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0002_auto_20211020_2241'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, max_length=250, verbose_name='Cart Id'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date_added',
            field=models.DateField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.cart', verbose_name='Cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='reduced_price',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Reduced Price'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation', verbose_name='Variations'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='category',
            field=models.ManyToManyField(to='category.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(blank=True, max_length=8, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='expires_in',
            field=models.DateTimeField(verbose_name='Expires In'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='is_used',
            field=models.BooleanField(default=False, null=True, verbose_name='Is Used'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='stock',
            field=models.IntegerField(verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='category',
            field=models.ManyToManyField(to='category.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='count',
            field=models.PositiveIntegerField(verbose_name='Count'),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='expires_in',
            field=models.DateTimeField(verbose_name='Expires In'),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='stock',
            field=models.IntegerField(verbose_name='Stock'),
        ),
    ]
