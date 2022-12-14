# Generated by Django 3.1 on 2021-12-06 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20211123_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Old Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='original_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Price'),
        ),
    ]
