# Generated by Django 3.2.9 on 2021-12-31 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20211231_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcart',
            name='is_supplier',
        ),
        migrations.AddField(
            model_name='customer',
            name='is_supplier',
            field=models.BooleanField(default=False, verbose_name='is Supplier'),
        ),
    ]
