# Generated by Django 3.2.9 on 2022-01-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_alter_customer_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True, verbose_name='Mobile Number'),
        ),
    ]
