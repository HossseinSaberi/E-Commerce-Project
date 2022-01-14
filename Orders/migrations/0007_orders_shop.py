# Generated by Django 3.2.9 on 2022-01-06 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0012_alter_category_category_parent'),
        ('Orders', '0006_auto_20211230_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='shop',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shop.shop', verbose_name='source shop'),
        ),
    ]
