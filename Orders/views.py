from cgi import print_environ
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView , UpdateView , TemplateView
from .forms import EditOrderDetails
from .models import Orders , OrderItems
from django.db.models.query_utils import Q
from .filters import OrderFilters
from django.db.models import Sum ,F

# Create your views here.

class ListOfOrders(LoginRequiredMixin , ListView):
    """this class show and handle list of order in manager"""
    model = Orders
    template_name = 'ManagerTemplate/OrderTemplate/ListOrder.html'
    context_object_name = 'all_Orders'
    filter_set = OrderFilters

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset=self.model.objects.filter(shop__supplier__customer__id = self.request.user.id)
        filter = OrderFilters(self.request.GET , queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_result = OrderFilters(self.request.GET , queryset=self.model.objects.filter(shop__supplier__customer__id = self.request.user.id))
        context['filter'] = filter_result
        return context

    

        queryset=Orders.objects.filter(shop__supplier__customer__id = self.request.user.id).values('update_at__day' , 'update_at__month').annotate(all_sold=Sum(F('product__price')*F('order_item__quantity')))
        queryset=Orders.objects.filter(shop__supplier__customer__id = self.request.user.id).values('update_at__day' , 'update_at__month').annotate(all_sold=Sum('total_price'))


def chart_data(request):
    labels = []
    data = []

    queryset=Orders.objects.filter(shop__supplier__customer__id = request.user.id).values('update_at__day' , 'update_at__month').annotate(all_sold=Sum(F('product__price')*F('order_item__quantity')))
    
    for order in queryset:
        labels.append(order['update_at__day'])
        data.append(order['all_sold'])

    return render(request, 'ManagerTemplate/OrderTemplate/ListOrderGraph.html', {
        'labels': labels,
        'data': data,
    })


class OrderDetail(LoginRequiredMixin , UpdateView):
    """this class is for edit status of orders by supplier"""
    model = Orders
    form_class = EditOrderDetails
    template_name = 'ManagerTemplate/OrderTemplate/EditOrder.html'
    success_url = '/manage_order/ListOrder/'
    context_object_name = 'form'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get(self.pk_url_kwarg)
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['order_details'] = OrderItems.objects.filter(order__id=id)
        return context


        
