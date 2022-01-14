from django.urls import path
from .views import ListOfOrders , OrderDetail , Chart

urlpatterns = [
    path('/ListOrder/', ListOfOrders.as_view() , name='ListOrder'),
    path('/ListOrderGraph/', Chart.as_view(), name='population-chart'),
    path('/<int:pk>/OrderDetails/', OrderDetail.as_view() , name='OrderDetail'),
]
