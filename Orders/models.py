from functools import total_ordering
from django.db import models 
from django.db.models  import F , Sum
from Users.models import Customer
from Shop.models import Product , Shop
from .manager import SubmitOrders , PaidOrders , DraftOrders

# Create your models here.


class Orders(models.Model):
    objects = models.Manager()
    submit_order = SubmitOrders()
    darft_order = DraftOrders()
    paied_order = PaidOrders()

    user = models.ForeignKey(Customer, verbose_name=(
        "Customer"), on_delete=models.CASCADE)
    order_create_date = models.DateTimeField(
        ("Order Date"), auto_now_add=True)
    discount_available = models.BooleanField(
        ("Discount Available"), default=False)
    discount = models.DecimalField(
        ("Discount Percent"), max_digits=4, decimal_places=1,default=0)
    product = models.ManyToManyField(Product , through='OrderItems')
    shop = models.ForeignKey(Shop, verbose_name=("source shop"), on_delete=models.CASCADE , null=True , blank=True)
    STATUS = [
        (1 , 'submited'),
        (2 , 'canceled'),
        (3 , 'draft'),
        (4 , 'Paied'),
    ]

    status = models.IntegerField(("Status"), choices=STATUS , default=3)
    update_at = models.DateTimeField(("Update at"),  auto_now_add=False, null=True , blank=True)

    class Meta:
        verbose_name = 'Order'

    def __str__(self):
        return f"{self.shop}-{self.user}"

class OrderItems(models.Model):

    order = models.ForeignKey(Orders,related_name='order_item' ,  verbose_name="Order Name", on_delete=models.CASCADE)

    quantity = models.IntegerField(("Quantity"))
    product = models.ForeignKey(Product, verbose_name=(
        "Product"), on_delete=models.CASCADE)



    class Meta:
        verbose_name = 'Order Item'


    @property
    def price(self):
        return self.quantity * self.product.price



    def __str__(self) -> str:
        return f"{self.product}"
class Payment(models.Model):
    payment_type = models.CharField(("Payment Type"), max_length=50)
    payment_date = models.DateTimeField(("Payment Date"), auto_now_add=True)
    payment_status = models.CharField(("Payment Status"), max_length=50)
