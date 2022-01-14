from django.urls import path
from .views import ListOfOrders , OrderDetail , chart_data

urlpatterns = [
    path('/ListOrder/', ListOfOrders.as_view() , name='ListOrder'),
    path('/ListOrderGraph/', chart_data, name='ListOrderGraph'),
    path('/<int:pk>/OrderDetails/', OrderDetail.as_view() , name='OrderDetail'),
]
