from django_filters import rest_framework as filters

from .models import Payment


class PaymentFilter(filters.FilterSet):

    start_date = filters.DateFilter(
        field_name="payment_date",
        lookup_expr="gte",
    )

    end_date = filters.DateFilter(
        field_name="payment_date",
        lookup_expr="lte",
    )

    payment_method = filters.CharFilter(
        field_name="payment_method",
    )

    status = filters.CharFilter(
        field_name="status",
    )

    member = filters.UUIDFilter(
        field_name="member_id",
    )

    class Meta:
        model = Payment
        fields = [
            "start_date",
            "end_date",
            "payment_method",
            "status",
            "member",
        ]