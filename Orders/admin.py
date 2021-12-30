from django.contrib import admin
from .models import OrderItems , Orders , Payment
# Register your models here.
admin.site.register(Orders) 
admin.site.register(OrderItems) 
admin.site.register(Payment) 