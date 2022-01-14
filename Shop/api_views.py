from django.db.models import query
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework import authentication, permissions
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django.shortcuts import get_object_or_404, render
from django_filters import rest_framework as rest_filter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (filters, generics, mixins, serializers, status,
                            views)
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from Users.models import Supplier
from .filters import ShopNameCategoryFilterApi, ShopNameProductFilterApi
from .models import Product, Shop
from .serializers import (AllShopCategoriesSerializer, EachShopProductList,
                          ProductCreateApiSerializer,
                          ProductDetailsApiSerializer,
                          ProductListApiSerializer, ShopCreateApiSerializer,
                          ShopDetailsApiSerializer, ShopListApiSerializer)


class GetAllCreateProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    filterset_class = ShopNameProductFilterApi
    parser_classes = [MultiPartParser, FileUploadParser]
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListApiSerializer
        elif self.request.method == 'POST':
            return ProductCreateApiSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = self.perform_create(serializer)
        response_serializer = ProductListApiSerializer(product)
        headers = self.get_success_headers(serializer.data)
        return Response({'Success': 'The Product Create Successfuly', 'Data': response_serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class GetDetailsEditDeleteProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsApiSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.shop.supplier.customer != request.user:
            return Response(data={'msg': 'this product owned by another user'}, status=400)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.shop.supplier.customer != request.user:
            return Response(data={'msg': 'this product owned by another user'}, status=400)
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.shop__supplier__customer)
        if instance.shop.supplier.customer != request.user:
            return Response(data={'msg': 'this product owned by another user'}, status=400)
        return super().delete(request, *args, **kwargs)

# class GetAllShop(generics.RetrieveAPIView):
#     queryset= Shop.objects.all()
#     serializer_class = ShopListApiSerializer


class CreateShop(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateApiSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShopListApiSerializer
        elif self.request.method == 'POST':
            return ShopCreateApiSerializer

    parser_classes = [MultiPartParser, FileUploadParser]

    def create(self, request, *args, **kwargs):
        # supplier = Supplier.objects.get(customer__id=self.kwargs['id'])
        serializer = ShopCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop = self.perform_create(serializer)
        # shop.supplier=supplier
        response_serializer = ProductListApiSerializer(shop)
        headers = self.get_success_headers(serializer.data)
        return Response({'Success': 'The Shop Create Successfuly', 'Data': response_serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class GetDetailsEditDeleteShop(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDetailsApiSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.supplier.customer != request.user:
            return Response(data={'msg': 'this shop owned by another user'}, status=400)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.supplier.customer != request.user:
            return Response(data={'msg': 'this shop owned by another user'}, status=400)
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.supplier.customer != request.user:
            return Response(data={'msg': 'this shop owned by another user'}, status=400)
        return super().delete(request, *args, **kwargs)


class GetAllSubmitShop(generics.ListAPIView):
    queryset = Shop.submitted_shop.all()
    filterset_class = ShopNameCategoryFilterApi
    serializer_class = ShopListApiSerializer


class GetShopAllProduct(generics.ListAPIView):

    queryset = Product.objects.all()
#   queryset = Shop.submitted_shop.all()
    serializer_class = EachShopProductList
    filter_backends = (filters.OrderingFilter, rest_filter.DjangoFilterBackend)
    filterset_class = ShopNameProductFilterApi
    filterset_fields = ('tag__title',)

    def filter_queryset(self, queryset):
        query = Product.objects.filter(shop_id=self.kwargs['id'])
        return super().filter_queryset(queryset=query)


class GetShopCategory (generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = AllShopCategoriesSerializer
