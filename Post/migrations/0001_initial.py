# Generated by Django 3.2.9 on 2021-12-29 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Category Title')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100, verbose_name='Comment Text')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at ')),
                ('author', models.CharField(max_length=100, verbose_name='UserName')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email')),
            ],
            options={
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tag Name')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Post Title')),
                ('shortDescription', models.CharField(max_length=100, verbose_name='Short Description')),
                ('Text', models.TextField(verbose_name='Text')),
                ('image', models.ImageField(blank=True, null=True, upload_to='postImages/', verbose_name='Image')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at ')),
                ('slug', models.SlugField(max_length=100, null=True, unique=True, verbose_name='Slug')),
                ('category', models.ManyToManyField(to='Post.Category')),
                ('tag', models.ManyToManyField(to='Post.Tag')),
            ],
        ),
    ]