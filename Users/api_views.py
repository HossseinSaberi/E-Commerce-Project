from logging import raiseExceptions
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, response
from rest_framework import generics, mixins, serializers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser , FileUploadParser
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from .models import Customer, Supplier
from .serializers import AllSupplierApiSerializer , AllCustomerApiSerializer , RegisterSerializerCustomer , ProfileSerializer


class GetAllCreateUser(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AllCustomerApiSerializer
        elif self.request.method == 'POST':
            return RegisterSerializerCustomer
    parser_classes = [MultiPartParser]
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'Success' : 'The User Create Successfuly'} , status = status.HTTP_201_CREATED , headers = self.headers)

class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Customer.objects.all()
    parser_classes = [MultiPartParser ]


# class LoginApi()