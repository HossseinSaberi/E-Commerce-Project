from rest_framework.test import APITestCase
from django.urls import reverse
from Shop.models import Product , Shop , Category , Tag
from .models import OrderItems, Orders
from Users.models import Customer , Supplier
from model_mommy import mommy
# Create your tests here.


class TestOrder(APITestCase):
    def setUp(self):
        
        self.customer = Customer(username='test' , password='1234' , email='test@test.com' , mobile_number='09111111111')
        self.customer.save()
        self.supplier = Supplier.objects.create(customer=self.customer, supplier_blog= 'testblog')
        self.category = Category.objects.create(category_title='test')
        self.tag = Tag.objects.create(title='test')

        self.single_shop = Shop(shop_name='test', shop_address='test',
                           shop_phone='1111111', supplier=self.supplier, category=self.category, status=1)
        self.single_shop.save()

        self.product = Product(product_name = 'test' , product_short_description='test' , price=100.00 , discount=10 , text='test' , slug='test' , stock=15 , shop = self.single_shop)
        self.product.save()
        self.product.tag.add(self.tag)
        self.product.category.add(self.category)

        self.order = Orders.objects.create(user = self.customer , shop = self.single_shop  , status = 2)
        self.order.save()

        self.submitted_order = mommy.make(Orders , status = 1 , user = self.customer , shop = self.single_shop , )


        self.order_item = OrderItems.objects.create(order = self.order , quantity = 1 , product = self.product)

    def test_order_list(self):
        url = reverse('api_GetAllOrder')
        self.client.force_authenticate(self.customer)
        resp = self.client.get(url)


        self.assertEquals(resp.status_code , 200)
        self.assertEquals(len(resp.data) , 2)


    def test_create_order(self):
        url = reverse('api_GetAllOrder')
        body = { 
            "discount": 10,
            "shop" : self.single_shop.id , 
            "quantity" : 10,
            "product" : self.product.id
        }
        self.client.force_authenticate(self.customer)
        resp = self.client.post(url , data=body)
        self.assertEquals(resp.status_code , 201)
        self.assertEquals(len(resp.data) , 2)


    def test_get_submitted_order(self):
        url = reverse('api_GetAllSubmitOrders')
        self.client.force_authenticate(self.customer)

        resp = self.client.get(url)
        self.assertEquals(resp.status_code , 200)
        self.assertEquals(len(resp.data) , 1)

    def test_set_paid_status(self):
        url = reverse('api_ChangeOrderStatus' , kwargs={'pk': self.order.id})
        self.client.force_authenticate(self.customer)

        resp = self.client.get(url)

        self.assertEquals(resp.status_code,200)
        self.assertEquals(resp.data['status'] , 4)


    def test_add_product_to_basket(self):
        url = reverse('api_AddProductToOrderItem')
        body = {
            "quantity" : 1,
            "product" : self.product.id,
            "order" : self.order.id
        }
        self.client.force_authenticate(self.customer)

        resp = self.client.post(url , data=body)

        self.assertEquals(resp.status_code , 201)


    def test_remove_product_from_basket(self):
        url = reverse('api_GetRemoveProductFromOrderItem' , kwargs={'pk': self.order_item.id})
        self.client.force_authenticate(self.customer)

        resp = self.client.delete(url)

        self.assertEquals(resp.status_code , 204)