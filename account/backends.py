import numbers
from Users.models import Customer
from django.contrib import messages
from django.contrib.auth import get_user_model
from .utils import check_mobile_number

from django.contrib.auth.backends import BaseBackend
User = get_user_model()

class EmailOrUsernameModelBackend(BaseBackend):

    def authenticate(self,request, username=None, password=None, **kwargs):
        print('worked!')
        
        if check_mobile_number(username):
            kwargs = {'mobile_number' : username}
        elif '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
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