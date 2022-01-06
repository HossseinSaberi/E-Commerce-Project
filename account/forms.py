from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import fields
from Users.models import Customer

User = get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='UserName')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput, label='Remember Me!', required=False)


class SignInForm(UserCreationForm):
    Email = forms.EmailField(label='Email')
    username = forms.CharField(max_length=50, label='UserName')

    class Meta:
        model = User
        fields = ('Email' , 'username' , 'password1' , 'password2' ,)


# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = Customer
#         fields = ('email',)


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = Customer
#         fields = ('email',)