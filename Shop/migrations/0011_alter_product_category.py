# Generated by Django 3.2.9 on 2022-01-03 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0010_auto_20220103_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='Shop.Category', verbose_name='Category'),
        ),
    ]
