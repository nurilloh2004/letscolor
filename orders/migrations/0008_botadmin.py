# Generated by Django 3.1 on 2021-11-24 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20211108_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=12)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
