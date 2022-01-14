from itertools import product
from django.core.validators import ProhibitNullCharactersValidator
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from Shop.serializers import TagSerializer
from .models import Tag, Category, Shop, Product
from Users.models import Supplier , Customer
from model_mommy import mommy
# Create your tests here.


class TestShop(APITestCase):
    def setUp(self):
        shop = mommy.make(Shop, status=2, _quantity=3)
        submit_shop = mommy.make(Shop, status=1, _quantity=3)


        customer = Customer(username='test' , password='1234' , email='test@test.com' , mobile_number='09111111111')
        customer.save()
        self.supplier = Supplier.objects.create(customer=customer, supplier_blog= 'testblog')
        self.category = Category.objects.create(category_title='test')
        self.tag = Tag.objects.create(title='test')

        self.single_shop = Shop(shop_name='test', shop_address='test',
                           shop_phone='1111111', supplier=self.supplier, category=self.category, status=1)
        self.single_shop.save()

        self.product = Product(product_name = 'test' , product_short_description='test' , price=100.00 , discount=10 , text='test' , slug='test' , stock=15 , shop = self.single_shop)
        self.product.save()
        self.product.tag.add(self.tag)
        self.product.category.add(self.category)

    def test_shop_list(self):
        url = reverse('api_CreateShop')
        resp = self.client.get(url)

        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.data), 7)

    def test_create_shop(self):
        url = reverse('api_CreateShop')
        body = {
            "shop_name": "test shop",
            "shop_address": "test address",
            "shop_phone": "11111111",
            "status": 1,
            "category": self.category.id,
            "supplier": self.supplier.id,
        }
        resp = self.client.post(url, data=body)
        all_shop = self.client.get(url)

        self.assertEquals(resp.status_code, 201)
        self.assertEquals(len(all_shop.data), 8)

    def test_submit_shop_list(self):

        url = reverse('api_GetAllSubmitShop')
        resp = self.client.get(url)

        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.data), 4)

    def test_edit_shop(self):
        shop = Shop(shop_name='test', shop_address='test',
                           shop_phone='1111111', supplier=self.supplier, category=self.category, status=1)
        shop.save()

        url = reverse('api_GetShopDetails', kwargs={'pk': shop.id})
        new_shop_Name = "new title"
        body = {
            "id":shop.id,
            "shop_name": new_shop_Name,
            "shop_address": "test address",
            "shop_phone": "11111111",
            "status": 1,
            "category": self.category.id,
            "supplier": self.supplier.id,
        }
        # self.client.force_authenticate(self.user)
        resp = self.client.patch(url, data = body)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["shop_name"], new_shop_Name)

    def test_get_shop(self):

        url = reverse('api_GetShopDetails', kwargs={'pk': self.single_shop.id})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    def test_delete_shop(self):
        all_url = reverse('api_CreateShop')
        all_shop = self.client.get(all_url)

        url = reverse('api_GetShopDetails', kwargs={'pk': self.single_shop.id})
        resp = self.client.delete(url)
        new_all_shop = self.client.get(all_url)
        self.assertEquals(resp.status_code, 204)
        self.assertEquals(len(new_all_shop.data), len(all_shop.data)-1)

    def test_shop_category(self):
        url = reverse('api_GetShopCategory')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code , 200)

class TestProduct(APITestCase):
    def setUp(self):
        customer = Customer(username='test' , password='1234' , email='test@test.com' , mobile_number='09111111111')
        customer.save()
        self.supplier = Supplier.objects.create(customer=customer, supplier_blog= 'testblog')
        self.category = Category.objects.create(category_title='test')
        self.tag = Tag.objects.create(title='test')

        self.single_shop = Shop(shop_name='test', shop_address='test',
                           shop_phone='1111111', supplier=self.supplier, category=self.category, status=1)
        self.single_shop.save()

        self.product = Product(product_name = 'test' , product_short_description='test' , price=100.00 , discount=10 , text='test' , slug='test' , stock=15 , shop = self.single_shop)
        self.product.save()
        self.product.tag.add(self.tag)
        self.product.category.add(self.category)


    def test_product_list(self):
        url = reverse('api_GetAllCreateProduct')
        resp = self.client.get(url)

        self.assertEquals(resp.status_code,200)
        self.assertEquals(len(resp.data) , 1)

    def test_create_product(self):
        url = reverse('api_GetAllCreateProduct')
        body = {
            "product_name": "test product",
            "product_short_description": "test Description",
            "price": "111.11",
            "discount_available": True,
            "discount": "10.0",
            "text": "test Text",
            # "slug": "test-slug",
            "stock": 10,
            "shop": self.single_shop.id,
            "tag":{self.tag.id , },
            "category" : {self.category.id ,}
            }
        resp = self.client.post(url , data = body)
        all_product = self.client.get(url)

        self.assertEquals(resp.status_code , 201)
        self.assertEquals(len(all_product.data) ,2)

    def test_get_product(self):
        url = reverse('api_GetProductDetails' , kwargs={'pk': self.product.id})
        resp = self.client.get(url)

        self.assertEquals(resp.status_code , 200)


    def test_edit_product(self):
        url = reverse('api_GetProductDetails' , kwargs={'pk': self.product.id})
        new_product_Name = "new name"
        body = {
            "product_name": new_product_Name,
        }
        # self.client.force_authenticate(self.user)
        resp = self.client.patch(url, data = body)
        self.assertEqual(resp.status_code, 200)

        # updated_product = Product.objects.get(id=self.single_shop.id)
        self.assertEqual(resp.data['product_name'], new_product_Name)

    def test_delete_product(self):
        all_url = reverse('api_GetAllCreateProduct')
        all_product = self.client.get(all_url)

        url = reverse('api_GetProductDetails' , kwargs={'pk': self.product.id})
        resp = self.client.delete(url)
        new_all_product = self.client.get(all_url)
        self.assertEquals(resp.status_code, 204)
        self.assertEquals(len(new_all_product.data), len(all_product.data)-1)
        