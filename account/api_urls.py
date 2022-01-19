from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls.static import static
from .api_views import DisposableCodeLogin

urlpatterns = [
    path('/DisposableCodeLogin/' , DisposableCodeLogin.as_view() , name='DisposableCodeLogin')    
    
]
