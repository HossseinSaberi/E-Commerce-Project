from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls.static import static
from .api_views import  GetListSubmitOrders , GetListDraftOrders , GetListPaiedOrders , CreateGetListOrders  , ChangeStatusOfOrder , AddProductToOrderItems , GetRemoveProductFromOrderItem


urlpatterns = [
	path('Order' , CreateGetListOrders.as_view() , name='api_GetAllOrder'),
	path('OrderItems' , AddProductToOrderItems.as_view() , name='api_AddProductToOrderItem'),
	path('OrderItems/<int:pk>' , GetRemoveProductFromOrderItem.as_view() , name='api_GetRemoveProductFromOrderItem'),
	path('SubmitOrder' , GetListSubmitOrders.as_view() , name='api_GetAllSubmitOrders'),
	path('DraftOrder' , GetListDraftOrders.as_view() , name='api_GetAllDraftOrders'),
	path('PaiedOrder' , GetListPaiedOrders.as_view() , name='api_GetAllPaiedOrders'),
	path('OrderStatus/<int:pk>' , ChangeStatusOfOrder.as_view() , name='api_ChangeOrderStatus'),
]