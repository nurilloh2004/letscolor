# Generated by Django 3.1 on 2021-10-20 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20211020_1803'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'verbose_name': 'OrderProduct', 'verbose_name_plural': 'OrderProducts'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
    ]
