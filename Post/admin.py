from django.contrib import admin
from .models import Post , Category , Comment , Tag
from django.utils.html import format_html

# Register your models here.

# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =('show_image','title' , 'shortDescription' , 'writer' , 'create_at' , 'updated_at')
    prepopulated_fields = {'slug':('title',)}


    def show_image(self, obj):
        if (obj.image):
            print(f'salam mamad {obj.image.url}')
        
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url
            )
        return '-'