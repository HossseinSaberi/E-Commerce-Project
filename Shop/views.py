from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.api import success
from django.db.models import fields
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView
from django.shortcuts import redirect
from Post.views import category, postDetails
from .models import Product, Shop, Category, Tag
from .forms import CreateOrEditCategory, CreateOrEditShopForm, CreateOrEditProductForm, CreateOrEditTag
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.


class MainManagerPage(TemplateView, DetailView):
    def get(self, request, *args, **kwargs):
        accepted_shop = Shop.submitted_shop.filter(
            supplier__customer__id=request.user.id).first()
        draft_shop = Shop.darft_shop.filter(
            supplier__customer__id=request.user.id).order_by('-update_at').reverse().first()
        deleted_shop = Shop.deleted_shop.filter(
            supplier__customer__id=request.user.id).order_by('-update_at').first()

        return render(request, 'ManagerTemplate/ShopDetails.html', {'accepted_shop': accepted_shop, 'draft_shop': draft_shop, 'deleted_shop': deleted_shop})


class CreateShop(LoginRequiredMixin, View):
    form = CreateOrEditShopForm

    def get(self, request, *args, **kwargs):
        return render(request, 'ManagerTemplate/AddShop.html', {'form': self.form, })

    def post(self, request, *args, **kwargs):
        user = request.user
        supplier = user.supplier_name
        shop_form = self.form(request.POST, request.FILES)
        print(shop_form)
        if shop_form.is_valid():

            created_shop = Shop.objects.create(shop_name=shop_form.cleaned_data['shop_name'], shop_address=shop_form.cleaned_data['shop_address'], shop_phone=shop_form.cleaned_data[
                                               'shop_phone'], shop_logo=shop_form.cleaned_data['shop_logo'], supplier=supplier, category=shop_form.cleaned_data['category'], status=2)

            messages.info(request, 'The Shop is Adding to Your Dashboard')

        return redirect('/manager/')

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        check_draft_shops_status = Shop.darft_shop.filter(
            supplier__customer__id=request.user.id)
        check_success_shops_status = Shop.submitted_shop.filter(
            supplier__customer__id=request.user.id)
        if check_draft_shops_status:
            messages.error(
                request, 'You have a shop thats not submitted from the administrator , please wait ...', extra_tags='danger')
            return redirect ('/manager/')

        if check_success_shops_status:
            messages.error(
                request, 'You cannot have a shop any more ! you have one of them !', extra_tags='danger')
            return redirect ('/manager/')


class EditShop(LoginRequiredMixin, UpdateView):
    model = Shop
    form_class = CreateOrEditShopForm
    template_name = 'ManagerTemplate/EditShop.html'
    # fields = ['shop_name', 'shop_phone' , 'shop_logo' , 'category' , 'shop_address']
    success_url = '/manager/'

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get(self.pk_url_kwarg)
        specific_shop = Shop.objects.get(id=id)
        specific_shop.status = 2
        specific_shop.save()
        return super().post(request, *args, **kwargs)


class DeleteShop(LoginRequiredMixin, UpdateView):
    model = Shop

    def get(self, request, *args, **kwargs):
        return render(request, 'ManagerTemplate/DeleteConfrim.html')

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get(self.pk_url_kwarg)
        specific_shop = Shop.objects.get(id=id)
        specific_shop.status = 3
        specific_shop.save()

        messages.info(request, 'The Shop is Delete from Your Dashboard')
        return redirect('/manager/')


###########################  Product Views #################################

class CreateProduct(LoginRequiredMixin, CreateView):
    """this class is for creating product from supplier of shop"""
    
    model = Product
    form_class = CreateOrEditProductForm
    template_name = 'ManagerTemplate/ProductTemplate/AddOrEditProduct.html'
    success_url = '/manager/ListProduct/'

    def product_exist(self , slug):
        try:
            query = Product.objects.filter(slug = slug).first()
            new_stock = query.stock
            query.delete()
            return new_stock
        except:
            return None

    def form_valid(self , form):
        self.object= form.save()
        product_state = self.product_exist(self.object.slug)
        if product_state:
            self.object.stock += product_state
        else:
            category_selected = form.cleaned_data['category']
            tag_selected = form.cleaned_data['tag']

            for cat_item in category_selected:
                self.object.category.add(cat_item.id)
            for tag_item in tag_selected:
                self.object.tag.add(tag_item)
            self.object.save()

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class EditProduct(LoginRequiredMixin, UpdateView):
    """this class help to edit the model of product that created by supplier"""
    
    model = Product
    form_class = CreateOrEditProductForm
    template_name = 'ManagerTemplate/ProductTemplate/AddOrEditProduct.html'
    # fields = ['shop_name', 'shop_phone' , 'shop_logo' , 'category' , 'shop_address']
    success_url = '/manager/ListProduct/'

    def form_valid(self , form):
        self.object= form.save()
        category_selected = form.cleaned_data['category']
        tag_selected = form.cleaned_data['tag']

        for cat_item in category_selected:
            self.object.category.add(cat_item.id)
        for tag_item in tag_selected:
            self.object.tag.add(tag_item)
        self.object.save()

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs



class ShowAllProduct(LoginRequiredMixin, ListView):
    """this class is for showing list of all product thats belong to a shop"""
    
    model = Product
    template_name = 'ManagerTemplate/ProductTemplate/ListProduct.html'
    context_object_name = 'all_Product'


class DeleteProduct(LoginRequiredMixin, DeleteView):
    """its for deleting some product """
    
    model = Product
    template_name = 'ManagerTemplate/ProductTemplate/DeleteProduct.html'
    success_url = '/manager/ListProduct/'

##################### CTEGORY VIEW #############################


class CreateCategory(LoginRequiredMixin, CreateView):
    """this class is for creating category of shop and product"""
    
    model = Category
    form_class = CreateOrEditCategory
    template_name = 'ManagerTemplate/CategoryTemplate/AddOrEditCategory.html'
    success_url = '/manager/'


class ShowAllCategory(LoginRequiredMixin, ListView):
    """its for showing all of category as a list to show them"""
    
    model = Category
    template_name = 'ManagerTemplate/CategoryTemplate/ListCategory.html'
    context_object_name = 'all_Category'


class DeleteCategory(LoginRequiredMixin, DeleteView):
    """its for delete every category"""
    
    model = Category
    template_name = 'ManagerTemplate/CategoryTemplate/DeleteCategory.html'
    success_url = '/manager/ListCategory/'


class EditCategory(LoginRequiredMixin, UpdateView):
    """this class help to edit categories"""
    
    model = Category
    template_name = 'ManagerTemplate/CategoryTemplate/AddOrEditCategory.html'
    form_class = CreateOrEditCategory
    success_url = '/manager/ListCategory/'


# Tags View #######################33


class CreateTag(LoginRequiredMixin, CreateView):
    """this class help to create tag for product"""
    
    model = Tag
    form_class = CreateOrEditTag
    template_name = 'ManagerTemplate/TagTemplate/AddOrEditTag.html'
    success_url = '/manager/ListTag/'


class ShowAllTag(LoginRequiredMixin, ListView):
    """this class is for handling to show all of tag"""
    
    model = Tag
    template_name = 'ManagerTemplate/TagTemplate/ListTag.html'
    context_object_name = 'all_tag'


class DeleteTag(LoginRequiredMixin, DeleteView):
    """delete specefic tag"""
    model = Tag
    template_name = 'ManagerTemplate/TagTemplate/DeleteTag.html'
    success_url = '/manager/ListTag/'


class EditTag(LoginRequiredMixin, UpdateView):
    """its for editing some tags"""
    model = Tag
    template_name = 'ManagerTemplate/TagTemplate/AddOrEditTag.html'
    form_class = CreateOrEditTag
    success_url = '/manager/ListTag/'
