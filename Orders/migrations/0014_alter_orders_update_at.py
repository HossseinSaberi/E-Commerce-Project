# Generated by Django 3.2.9 on 2022-01-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0013_orders_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='update_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Update at'),
        ),
    ]
