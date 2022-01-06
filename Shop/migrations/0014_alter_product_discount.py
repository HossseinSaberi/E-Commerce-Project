# Generated by Django 3.2.9 on 2022-01-06 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0013_alter_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='Discount Percent'),
        ),
    ]
