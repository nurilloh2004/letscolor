# Generated by Django 3.1 on 2021-11-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_brand_brandtranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
