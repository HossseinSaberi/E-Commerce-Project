from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls.static import static
from .api_views import GetAllCreateUser , Profile

urlpatterns = [
	path('Users' , GetAllCreateUser.as_view() , name='api_GetAllCreateUser'),
	path('Profile/<int:pk>' , Profile.as_view() , name='api_Profile'),
]