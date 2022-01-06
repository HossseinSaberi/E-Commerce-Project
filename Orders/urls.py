from django.urls import path
from .views import ListOfOrders , OrderDetail

urlpatterns = [
    path('/ListOrder/', ListOfOrders.as_view() , name='ListOrder'),
    path('/<int:pk>/OrderDetails/', OrderDetail.as_view() , name='OrderDetail'),
]
