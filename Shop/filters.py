from random import choice
from django.db.models import fields
from django.db.models.enums import Choices
import django_filters
from .models import Category, Product, Shop

class ShopNameProductFilterApi(django_filters.FilterSet):
    shop_name = django_filters.CharFilter(field_name='shop__shop_name' , lookup_expr='icontains')
    category_title = django_filters.CharFilter(field_name='category__category_title' , lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['shop_name' , 'category_title']


class ShopNameCategoryFilterApi(django_filters.FilterSet):

    # all_category = Category.objects.filter(category_parent=None)
    # FILTER_CHOICE = []
    # for each_cat in all_category:
    #     cat_tuple = (each_cat.id , each_cat.category_title)
    #     FILTER_CHOICE.append(cat_tuple)


    shop_name = django_filters.CharFilter(field_name='shop_name' , lookup_expr='icontains')
    category_title = django_filters.CharFilter(field_name='category__category_title' , lookup_expr='icontains') #django_filters.ChoiceFilter(choices = FILTER_CHOICE)
    class Meta:
        model = Shop
        fields = ['shop_name' , 'category_title']


# class ShopNameProductFilterApi(django_filters.FilterSet):
#     tag = django_filters.CharFilter(field_name = 'product_shop_name__tag__title' , lookup_expr = 'icontains')

#     class Meta:
#         model = Shop
#         fields = ['tag']
        
class ShopNameProductFilterApi(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name = 'tag__title' , lookup_expr = 'icontains')
    # price = django_filters.OrderingFilter(choices='price')

    class Meta:
        model = Product
        fields = ['tag']