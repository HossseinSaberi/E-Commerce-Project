import django_filters

from Orders.models import Orders

class OrderFilters(django_filters.FilterSet):
    begin_date = django_filters.DateFilter(field_name='update_at' , lookup_expr='gt')
    end_date = django_filters.DateFilter(field_name='update_at' , lookup_expr='lt')
    date_range = django_filters.DateRangeFilter(field_name='update_at')

    class Meta:
        model = Orders
        fields = ['status' , 'begin_date' , 'end_date']