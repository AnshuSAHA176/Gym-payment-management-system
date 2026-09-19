from django_filters import rest_framework as filters
from .models import Payment

class PaymentFilter(filters.FilterSet):
    
    date_range = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Payment
        fields = ['date_range']