# Generated by Django 3.2.9 on 2021-12-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20211229_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='is_supplier',
        ),
        migrations.AddField(
            model_name='creditcart',
            name='is_supplier',
            field=models.BooleanField(default=False, verbose_name='is Supplier'),
        ),
    ]
