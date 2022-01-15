from itertools import product
from operator import ge
from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import tree
from rest_framework import generics, mixins, serializers
from rest_framework.response import Response
from rest_framework import status
from Shop.models import Product , Shop
from rest_framework.parsers import MultiPartParser
from Users.models import Customer
from .models import OrderItems, Orders
from .serializers import OrderListApiSerializer , OrdersCreateApiSerializer , OrderDetailsApiSerializer , AddOrderItemsApiSerializers , ListOrderItems
from rest_framework import authentication, permissions

class CreateGetListOrders(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    parser_classes = [MultiPartParser]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListApiSerializer
        elif self.request.method == 'POST':
            return OrdersCreateApiSerializer


    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        shop = Shop.objects.get(id=request.data['shop'])
        new_order = Orders.objects.create(user=request.user , discount=request.data['discount'] , shop=shop)
        orderitems_body = {'quantity':request.data['quantity'], 'order' : new_order.id , 'product' : request.data['product']}
        serializer = AddOrderItemsApiSerializers(data=orderitems_body)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id = request.data['product'])
        if int(product.stock) < int(request.data['quantity']):
            return Response({'Error': 'The Order items request quantity is more than stock'}, status=status.HTTP_400_BAD_REQUEST)
        product.stock = int(product.stock) - int(request.data['quantity'])
        product.save()
        orderitems = self.perform_create(serializer)
        response_serializer = ListOrderItems(orderitems)
        headers = self.get_success_headers(serializer.data)
        return Response({'Success': 'The Order items Added Successfuly', 'Data': response_serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class GetListSubmitOrders(generics.ListAPIView):

    queryset =  Orders.submit_order.all()
    serializer_class = OrderListApiSerializer


class GetListDraftOrders(generics.ListAPIView):

    queryset =  Orders.darft_order.all()
    serializer_class = OrderListApiSerializer


class GetListPaiedOrders(generics.ListAPIView):

    queryset =  Orders.paied_order.all()
    serializer_class = OrderListApiSerializer


# class ChangeStatusOfOrder(generics.UpdateAPIView):
#     queryset = Orders.objects.all()
#     serializer_class = OrderDetailsApiSerializer
#     parser_classes = [MultiPartParser]


class ChangeStatusOfOrder(generics.RetrieveAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderDetailsApiSerializer

    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.status = 4
        instance.save()
        return Response(serializer.data)

    
class AddProductToOrderItems(generics.ListCreateAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = AddOrderItemsApiSerializers
    parser_classes = [MultiPartParser]

    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = AddOrderItemsApiSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id = request.data['product'])
        if int(product.stock) < int(request.data['quantity']):
            return Response({'Error': 'The Order items request quantity is more than stock'}, status=status.HTTP_400_BAD_REQUEST)
        product.stock = int(product.stock) - int(request.data['quantity'])
        product.save()
        orderitems = self.perform_create(serializer)
        response_serializer = ListOrderItems(orderitems)
        headers = self.get_success_headers(serializer.data)
        return Response({'Success': 'The Order items Added Successfuly', 'Data': response_serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class GetRemoveProductFromOrderItem(generics.RetrieveDestroyAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = ListOrderItems

    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.product.stock+=instance.quantity
        instance.product.save()
        order_id = instance.order.id
        instance.delete()
        other_order = OrderItems.objects.filter(order__id = order_id)
        if len(other_order) == 0:
            order = Orders.objects.get(id = order_id)
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
