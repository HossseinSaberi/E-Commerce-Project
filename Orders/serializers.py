from itertools import product
from django.db.models import fields
from rest_framework import serializers
from .models import OrderItems, Orders
from drf_writable_nested.serializers import WritableNestedModelSerializer

class OrderListApiSerializer(serializers.ModelSerializer):
    update_at = serializers.DateTimeField(format="%Y-%m-%d",read_only = True)
    order_create_date = serializers.DateTimeField(format="%Y-%m-%d",read_only = True)
    
    class Meta:
        model = Orders
        fields = '__all__'

class OrderItemsApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['quantity' , 'product']

class OrdersCreateApiSerializer(WritableNestedModelSerializer , serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    product = serializers.IntegerField()
    class Meta:
        model = Orders
        fields = ['shop' , 'discount' , 'quantity' , 'product']


class OrderDetailsApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['status' , ]


class AddOrderItemsApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class ListOrderItems(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'
