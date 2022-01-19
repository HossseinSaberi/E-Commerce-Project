from django import forms
from django.db import models
from django.db.models import fields
from django.forms import widgets

from .models import OrderItems , Orders

class EditOrderDetails(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status' , 'discount' , 'user' , 'shop']