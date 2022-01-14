from os import set_inheritable
from django.db.models import fields
from rest_framework import serializers

from .models import Category, Product, Shop, Tag
from Users.serializers import SupplierDetailsApiSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_title', 'category_parent']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']


class ProductListApiSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    tag = TagSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'discount',
                  'slug', 'stock', 'shop', 'category' , 'tag']

        
class EachShopProductList(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'shop' , 'price' , 'slug' , 'tag']


class ShopListApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'shop_name', 'shop_phone', 'supplier', 'category']


class AllProductOfShop(serializers.ModelSerializer):
    shop = ShopListApiSerializer()
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'discount',
                  'slug', 'stock', 'shop', 'category']


class ShopCreateApiSerializer(serializers.ModelSerializer):
    shop_logo = serializers.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = Shop
        fields = '__all__'


class ProductCreateApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailsApiSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    category = CategorySerializer(many=True)
    product_main_image = serializers.ImageField(allow_empty_file=True, required=True)

    class Meta:
        model = Product
        fields = '__all__'


class ShopDetailsApiSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    supplier = SupplierDetailsApiSerializer()

    class Meta:
        model = Shop
        fields = '__all__'


class AllShopCategoriesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Shop
        fields = ['shop_name','category']
