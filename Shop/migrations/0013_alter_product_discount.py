# Generated by Django 3.2.9 on 2022-01-06 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0012_alter_category_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.FloatField(default=0, verbose_name='Discount Percent'),
        ),
    ]
