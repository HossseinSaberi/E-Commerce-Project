# Generated by Django 3.2.9 on 2022-01-02 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0007_auto_20220102_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_logo',
            field=models.ImageField(blank=True, null=True, upload_to='shopImage/', verbose_name='Image Logo'),
        ),
    ]
