# Generated by Django 3.2.9 on 2021-12-29 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitems',
            options={'verbose_name': 'Order Item'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name': 'Order'},
        ),
    ]
