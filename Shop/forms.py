from django import forms
from django.db import models
from django.db.models import fields
from django.forms import widgets
from .models import Category, Product, Shop, Tag

class CreateOrEditShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_name' , 'shop_address' , 'shop_phone' , 'shop_logo' , 'category')

    def __init__(self, *args, **kwargs):
        super(CreateOrEditShopForm, self).__init__(*args, **kwargs)
        self.fields['category']=forms.ModelChoiceField(queryset=Category.objects.filter(category_parent = None))


class DeleteShopForm(forms.Form):
    class Meta:
        model = Shop
        fields = []


class CreateOrEditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','slug','product_short_description','text','product_main_image','price','discount_available','discount','stock','tag' , 'category' , 'shop')
        
    def __init__(self, user ,  *args, **kwargs):
            super(CreateOrEditProductForm, self).__init__(*args, **kwargs)
            self.fields['shop'] = forms.ModelChoiceField(queryset= Shop.submitted_shop.filter(supplier__customer=user))

class CreateOrEditCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CreateOrEditTag(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class DeleteProductForm(forms.Form):
    class Meta:
        model = Product
        fields = []