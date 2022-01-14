from django.db import models
from Users.models import Customer, Supplier
from django.utils.text import slugify
# Create your models here.
import os
import uuid


class Category(models.Model):
    title = models.CharField('Category Title', max_length=50)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_DEFAULT , default="", related_name='sub_category')
    class Meta:
        verbose_name = 'Post Categorie'
    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField('Tag Name', max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):

    title = models.CharField('Post Title', max_length=100, unique=True)
    shortDescription = models.CharField('Short Description', max_length=100)
    Text = models.TextField('Text')
    image = models.ImageField(
        'Image', upload_to='postImages/', null=True, blank=True)
    create_at = models.DateTimeField('Create at ', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at ', auto_now=True)
    writer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField('Slug', max_length=100, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Comment Text', max_length=100)
    create_at = models.DateTimeField('Create at ', auto_now_add=True)
    author = models.CharField('UserName', max_length=100)
    email = models.EmailField('Email', null=True, blank=True, max_length=100)
    post = models.ForeignKey(
        Post, related_name='comment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_at']

    def __str__(self):
        return f"{self.author}'s comment for {self.post.title}"
