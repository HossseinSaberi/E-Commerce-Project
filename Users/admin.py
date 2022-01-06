from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Customer , CreditCart , Supplier
# Register your models here.

class CustomerAdmin(UserAdmin):

    model = Customer
    search_fields = ('username',)
    list_display = ('show_image','first_name','last_name','username' , 'email')
    # fields=(('username' , 'password') , ('first_name' , 'last_name'))
    fieldsets = (
        ( None , {
            'classes' : ('wide',),
            'fields' : (('username' , 'password') , ('first_name' , 'last_name') , ('email' , 'mobile_number') , ('user_image', 'age' , 'is_supplier')),
     }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('username','email'), ('password1', 'password2'), ('is_staff', 'is_active'))}
        ),
    )
    def show_image(self, obj):
        if (obj.user_image):
            print(f'salam mamad {obj.user_image.url}')
        
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.user_image.url
            )
        return '-'

admin.site.register(Customer,CustomerAdmin)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_blog',  'customer')
    fields=(('supplier_blog' , 'customer' ),)

@admin.register(CreditCart)
class CreditCartAdmin(admin.ModelAdmin):
    list_display = ('title' , 'user')
    fields=(('title' , 'user') , ('cart_number' , 'cvv2') , ('expiry_year' , 'expiry_Month'))
    list_filter=('user',)