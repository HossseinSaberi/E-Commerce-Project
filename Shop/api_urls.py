from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls.static import static
from .api_views import  CreateShop , GetAllCreateProduct , GetDetailsEditDeleteProduct , GetDetailsEditDeleteShop , GetAllSubmitShop , GetShopAllProduct , GetShopCategory

urlpatterns = [
	path('Product' , GetAllCreateProduct.as_view() , name='api_GetAllCreateProduct'),
	path('Product/<int:pk>/' , GetDetailsEditDeleteProduct.as_view() , name='api_GetProductDetails'),
	path('SubmitShop' , GetAllSubmitShop.as_view() , name='api_GetAllSubmitShop'),
	path('Shop/<int:id>/Product' , GetShopAllProduct.as_view() , name='api_GetShopAllProduct'),
	path('Shop' , CreateShop.as_view() , name='api_CreateShop'),
	path('Shop/<int:pk>/' , GetDetailsEditDeleteShop.as_view() , name='api_GetShopDetails'),
	path('Shop/Category/' , GetShopCategory.as_view() , name='api_GetShopCategory'),


	#TODO
	#FIX UPLOAD FILE FEATURE
	#SET FILTER ON SOME OF THEM
	#FINISH UNTIL THE POINT STEP OR MORE
]
