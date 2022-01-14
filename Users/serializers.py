from importlib.metadata import requires
from django.db.models import fields
from rest_framework import serializers, validators

from .models import Customer, Supplier

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id' , 'username' , 'email' , 'is_supplier']

class AllSupplierApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierDetailsApiSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Supplier
        fields = '__all__'

class AllCustomerApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id' , 'username' , 'email' , 'is_supplier'  , 'first_name' , 'last_name' , 'mobile_number']


class RegisterSerializerCustomer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True , validators = [validators.UniqueValidator(Customer.objects.all())])
    password = serializers.CharField(write_only=True , required = True )
    mobile_number = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = ['username' , 'email' , 'password'  , 'mobile_number']


    def create(self, validated_data):
        customer = Customer.objects.create(
            username = validated_data['username'],
            email = validated_data['email'] , 
            mobile_number = validated_data['mobile_number']
        )
        customer.set_password(validated_data['password'])
        customer.save()

        return customer


class ProfileSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(required = False)
    password = serializers.CharField(write_only=True , required=True)
    class Meta:
        model = Customer
        exclude = ['last_login' , 'date_joined' , 'groups' , 'user_permissions']

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()

        return instance