from functools import total_ordering
from django.db import models
from Users.models import Customer
from Shop.models import Product

# Create your models here.


class Orders(models.Model):
    user = models.ForeignKey(Customer, verbose_name=(
        "Customer"), on_delete=models.CASCADE)
    total_price = models.DecimalField(
        ("Total Price"), max_digits=5, decimal_places=2)
    status = models.CharField(("Status"), max_length=50)
    order_create_date = models.DateTimeField(
        ("Order Date"), auto_now_add=True)
    discount_available = models.BooleanField(
        ("Discount Available"), default=False)
    discount = models.DecimalField(
        ("Discount Percent"), max_digits=3, decimal_places=2, default=0)


    STATUS = [
        (1 , 'submited'),
        (2 , 'canceled'),
        (3 , 'deleted'),
    ]

    status = models.IntegerField(("Status"), choices=STATUS , default=1)

    class Meta:
        verbose_name = 'Order'


class OrderItems(models.Model):

    order = models.ForeignKey(Orders, verbose_name=(
        "Order Name"), on_delete=models.CASCADE)

    quantity = models.IntegerField(("Quantity"))
    price = models.DecimalField(
        ("Price"), max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product, verbose_name=(
        "Product"), on_delete=models.CASCADE)



    class Meta:
        verbose_name = 'Order Item'


class Payment(models.Model):
    payment_type = models.CharField(("Payment Type"), max_length=50)
    payment_date = models.DateTimeField(("Payment Date"), auto_now_add=True)
    payment_status = models.CharField(("Payment Status"), max_length=50)
