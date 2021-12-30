from django.contrib import admin
from .models import Category, Feature, Tag, Shop, Product, SubImage
from django.utils.html import format_html
# Register your models here.

admin.site.register(Tag)
admin.site.register(SubImage)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
        list_display = ('title' , 'value')
        fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('title' , 'value'),),
        }
        ),
    )


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('show_image', 'shop_name', 'supplier', 'category')

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('shop_name', 'supplier'), 'shop_address', ('shop_logo', 'category' , 'status')),
        }
        ),
    )

    @admin.display(empty_value='-', description="show image")
    def show_image(self, obj):
        if (obj.shop_logo):
            print(obj.shop_logo.url)

            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.shop_logo.url,

            )
        return '-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('show_image' , 'product_name', 'shop', 'price', 'created_at', 'update_at')
    prepopulated_fields = {'slug': ('product_name', 'shop')}
    list_filter = ('shop','product_name')

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('product_name', 'price'), ('shop', 'slug', 'stock'), ('product_main_image', ), ('discount_available', 'discount'), ('text', 'product_short_description'), 'tag'),
        }
        ),
    )
    def show_image(self, obj):
        if (obj.product_main_image):
            print(obj.product_main_image.url)

            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.product_main_image.url,

            )
        return '-'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('show_image', 'category_title', 'category_parent')
    fieldsets = (
        (None, {
            "fields": (
                ('category_title', 'category_parent'), 'category_image'
            ),
        }),
    )

    def show_image(self, obj):
        if (obj.category_image):
            print(obj.category_image.url)

            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.category_image.url,

            )
        return '-'
