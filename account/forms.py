from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import fields

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

    # def clean(self):
    #     cleaned_data = super(SignInForm, self).clean()
    #     email = cleaned_data.get("Email")
    #     username = cleaned_data.get("username")
    #     # password = cleaned_data.get("password")
    #     # re_password = cleaned_data.get("re_password")

    #     # if password != re_password:
    #     #     raise forms.ValidationError(
    #     #         'Password and RePassword does not match !')
