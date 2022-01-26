from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from .managers import CustomUserManager , SupplierManager , ActiveManager
# Create your models here.
PHONE_NUMBER_REGEX = RegexValidator(r'^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$')

class Customer (AbstractUser):
    objects = CustomUserManager()
    suppliers = SupplierManager()
    active = ActiveManager()

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    user_image = models.ImageField(
        'Profile Image',  upload_to='customerImage/', null=True, blank=True)
    address = models.TextField('Address',  null=True, blank=True)
    age = models.IntegerField(("Age"),  null=True, blank=True)
    mobile_number = models.CharField(
        ("Mobile Number"), max_length=15, unique=True ,  validators=[PHONE_NUMBER_REGEX])
    is_supplier = models.BooleanField(("is Supplier"), default=False)
    is_mobile_submitted = models.BooleanField(("is mobile submitted") , default=False)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class CreditCart(models.Model):
    title = models.CharField(("Cart Tilte"), max_length=50)
    user = models.ForeignKey(Customer, verbose_name=(
        "Customer"), on_delete=models.CASCADE)
    cart_number = models.CharField(("Cart Number"), max_length=16)
    cvv2 = models.IntegerField(("CVV2"))
    expiry_year = models.IntegerField(("Year"))
    expiry_Month = models.IntegerField(("Month"))
    

    def __str__(self):
        return f"{self.user}' '{self.title}"


class Supplier(models.Model):
    customer = models.OneToOneField(Customer, verbose_name=(
        "Customer"), on_delete=models.CASCADE, null=True, blank=True , related_name='supplier_name')
    supplier_blog = models.CharField(("Blog"), max_length=30)


    class Meta:
        verbose_name = 'Supplier'

    def __str__(self):
        return self.customer.username
