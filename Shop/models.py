from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model
from django.utils import text, tree
from django.utils.text import slugify
from Users.models import Supplier
from .managers import SubmittedShopManager , DeletedShopManager , DraftShopManager

# Create your models here.


class Category(models.Model):
    category_title = models.CharField(
        verbose_name='Category Title', max_length=50)
    category_image = models.ImageField(
        verbose_name='Category Image',  upload_to='categoryImage/', height_field=None, width_field=None)
    category_parent = models.ForeignKey(
        "self", verbose_name='Parent', null=True, blank=True, related_name='sub_category', on_delete=models.SET_DEFAULT , default="")

    class Meta:
        verbose_name = 'Categorie'

    def __str__(self):
        return self.category_title


class Feature(models.Model):
    title = models.CharField('Feature Title', max_length=50)
    value = models.CharField('Feature Value', max_length=100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField('Tag Name', max_length=100)

    def __str__(self):
        return self.title


class Shop(models.Model):

    STATUS = [
        (1 , 'submited'),
        (2 , 'draft'),
        (3 , 'deleted'),
    ]
    objects = models.Manager()
    submitted_shop = SubmittedShopManager()
    darft_shop = DraftShopManager()
    deleted_shop = DeletedShopManager()

    shop_name = models.CharField(verbose_name='Shop Name', max_length=50)
    shop_address = models.TextField(
        verbose_name='Shop Address', max_length=200)
    shop_phone = models.CharField(verbose_name='Shop Phone', max_length=12)
    shop_logo = models.ImageField(
        verbose_name='Image Logo',  upload_to='shopImage/', null=True , blank=True)

    supplier = models.ForeignKey(
        Supplier, verbose_name='Supplier', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(
        Category, verbose_name='Category', on_delete=models.PROTECT)

    created_at = models.TimeField(("Created at"), auto_now_add=True , blank=True , null=True)
    update_at = models.TimeField(("Update at"), auto_now_add=True , blank=True , null=True)

    status = models.IntegerField(("Status") , choices=STATUS , default=1)
    def __str__(self):
        return self.shop_name




class Product(models.Model):
    product_name = models.CharField('Product Name', max_length=50)
    product_short_description = models.TextField('Product Short Description')
    product_main_image = models.ImageField(
        'Product Main Image',  upload_to='productImage/', height_field=None, width_field=None)
    price = models.DecimalField(
        'Product Price', max_digits=9, decimal_places=2)
    discount_available = models.BooleanField(
        'Discount Available', default=False)
    discount = models.DecimalField(
        'Discount Percent', max_digits=4, decimal_places=1, default=0)
    text = models.TextField('Product Main Text')
    created_at = models.DateField(
        'Created At', auto_now_add=True)
    update_at = models.DateField('Update At', auto_now_add=True)
    slug = models.SlugField('Slug' , null=True , blank=True)
    stock = models.IntegerField('Number Of Product', default=0)
    shop = models.ForeignKey(Shop, verbose_name='Shop',
                             on_delete=models.CASCADE, related_name='product_shop_name')
    tag = models.ManyToManyField(Tag, verbose_name=("Tags"))
    category = models.ManyToManyField(
        Category, verbose_name='Category')

    def save(self, *args, **kwargs):
        complete_slug = f"{self.product_name}-{self.shop}"
        complete_slug = complete_slug.replace(" ","-")
        self.slug = slugify(complete_slug)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name + ' from '+self.shop.shop_name

    @property
    def calculate_discount(self):
        return self.price-(self.price*self.discount/100)

    
    # def calculate_stock(self , number):
    #     if self.stock  


    ######## Calculate Stock #######


class Comment(models.Model):
    comment_text = models.TextField('Comment Text')
    email = models.EmailField(("Email_Address"), max_length=254)
    create_at = models.DateTimeField(
        'Created At', auto_now_add=True)
    reply_comment = models.ForeignKey(
        'self', verbose_name='Reply Comment', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name='Product', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_at']

    def __str__(self):
        return f"{self.author}'s comment for {self.product.product_name}"


class SubImage(models.Model):
    sub_image = models.ImageField(
        'Sub Images',  upload_to='productImage/', height_field=None, width_field=None)
    product = models.ForeignKey(
        Product, verbose_name='Product', on_delete=models.CASCADE)

    def __str__(self):
        return f'Sub Images of {self.product}'
