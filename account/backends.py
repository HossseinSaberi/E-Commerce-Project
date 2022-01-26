import code
import numbers
from Users.models import Customer
from django.contrib import messages
from django.contrib.auth import get_user_model
from .utils import check_mobile_number
import redis
from initial_DataBase import REDIS_OTP_PORT, REDIS_OTP_HOST
from django.contrib.auth.backends import BaseBackend
User = get_user_model()

class EmailModelBackend(BaseBackend):

    def authenticate(self,request, username=None, password=None, **kwargs):
        kwargs = {'email': username}
        try:
            user = Customer.objects.get(**kwargs)
            if user.check_password(password) is True:
                return user
            messages.error(request, f"The UserName or Password is Wrong !", extra_tags='danger')
        except Customer.DoesNotExist:
            pass

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class UserNameModelBackend(BaseBackend):
    def authenticate(self, request, username=None , password=None, **kwargs):
        kwargs = {'username' : username}
        try:
            user = Customer.objects.get(**kwargs)
            if user.check_password(password) is True:
                return user
            messages.error(request, f"The UserName or Password is Wrong !", extra_tags='danger')
        except Customer.DoesNotExist:
            pass

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class MobileModelBackend(BaseBackend):
    def authenticate(self, request, username=None , password=None, **kwargs):
        kwargs = {'mobile_number' : username}
        try:
            user = Customer.objects.get(**kwargs)
            if user.is_supplier :
                if user.check_password(password) is True:
                    return user
                messages.error(request, f"The UserName or Password is Wrong !", extra_tags='danger')
            else:
                messages.error(request , f"you cant login with this method because you are not a supplier ...")
        except Customer.DoesNotExist:
            pass

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class OneTimeMobilePassword(BaseBackend):
    redis_client = redis.Redis(host=REDIS_OTP_HOST, port=REDIS_OTP_PORT)
    def check_mobile_exist(self , mobile):
        code = self.redis_client.get(mobile)
        if code:
            return code.decode()
        return None

    def check_code(self , mobile , code):
        coincidence_code = self.check_mobile_exist(mobile)
        if coincidence_code == code:
            return True
        return False

    def get_user(self,mobile):
        try:
            return User.objects.get(mobile_number=mobile)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None , password=None, **kwargs):
        correct_password = self.check_code(username , password)
        if correct_password :
            get_user_details = self.get_user(username)
            if get_user_details :
                return get_user_details
            else :
                return None
        
        