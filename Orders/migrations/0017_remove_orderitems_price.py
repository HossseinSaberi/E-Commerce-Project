# Generated by Django 3.2.9 on 2022-01-13 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0016_alter_orderitems_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='price',
        ),
    ]