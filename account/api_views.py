from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework import generics, mixins, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken 
from Users.models import Customer 
from .utils import check_activate

class DisposableCodeLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



# class AcceptMobile(generics.UpdateAPIView):
#     serializer_class = ''
#     queryset = Customer.active.all()

#     def patch(self, request, *args, **kwargs):
#         user = self.get_object()

#         if not check_activate(user):

#         return super().patch(request, *args, **kwargs)
