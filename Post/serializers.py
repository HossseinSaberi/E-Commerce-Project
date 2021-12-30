from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Category, Comment, Post


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    parentCategory = ParentCategorySerializer(source = 'parent' , read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'parentCategory']

        def get_related_field(self, model_field):
            return CategorySerializer()


class AllPostSerializer(serializers.ModelSerializer):

    writer = UserSerializer()
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['title', 'shortDescription', 'create_at',
                  'updated_at', 'writer', 'slug', 'category']


class PostDetailsSerializer(serializers.ModelSerializer):
    writer = UserSerializer()
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['title', 'shortDescription', 'create_at',
                  'updated_at', 'writer', 'slug', 'category']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostDetailsSerializer(serializers.ModelSerializer):
    writer = UserSerializer()
    category = CategorySerializer(read_only=True, many=True)
    comment = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['title', 'shortDescription', 'create_at',
                  'updated_at', 'writer', 'slug', 'category', 'comment']
