# Generated by Django 3.2.9 on 2021-12-29 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
    ]
