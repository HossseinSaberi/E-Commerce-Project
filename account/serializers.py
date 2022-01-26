from os import set_inheritable
from wsgiref.validate import validator
from django.db.models import fields
from rest_framework import serializers, validators

from Users.models import Customer , PHONE_NUMBER_REGEX

class PhoneSerializer(serializers.Serializer):    
    mobile_number = serializers.CharField(validators = [PHONE_NUMBER_REGEX,])
        
class ActivateAccountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length = 5 , min_length = 5)
    mobile_number = serializers.CharField(validators = [PHONE_NUMBER_REGEX,])