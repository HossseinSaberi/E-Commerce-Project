from cProfile import label
from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import fields
from Users.models import Customer , PHONE_NUMBER_REGEX

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='UserName')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput, label='Remember Me!', required=False)


class SignInForm(UserCreationForm):
    Email = forms.EmailField(label='Email')
    username = forms.CharField(max_length=50, label='UserName')
    mobile_number = forms.CharField(label='Moblie' , validators=[PHONE_NUMBER_REGEX])

    class Meta:
        model = Customer
        fields = ('Email' , 'username' , 'password1' ,'password2' , 'mobile_number')


class MobileLoginForm(forms.Form):
    mobile_number = forms.CharField(label='MobileNumber' , validators=[PHONE_NUMBER_REGEX])
