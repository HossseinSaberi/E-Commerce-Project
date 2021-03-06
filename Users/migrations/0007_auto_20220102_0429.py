# Generated by Django 3.2.9 on 2022-01-02 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_auto_20220101_0549'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customer',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='supplier',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_name', to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
    ]
