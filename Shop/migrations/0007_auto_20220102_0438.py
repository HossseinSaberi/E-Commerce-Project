# Generated by Django 3.2.9 on 2022-01-02 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0006_alter_shop_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='created_at',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='Created at'),
        ),
        migrations.AddField(
            model_name='shop',
            name='update_at',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='Update at'),
        ),
    ]
