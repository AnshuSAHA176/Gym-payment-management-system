from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend

from .models import Payment
from .serializer import PaymentSerializer, PaymentCreateSerializer
from .filters import PaymentFilter
import calendar

class PaymentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50


class PaymentView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Payment.objects.select_related("member")

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        "member__name",
        "member__phone",
        "member__member_id",
    ]

    filterset_class = PaymentFilter
    pagination_class = PaymentPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PaymentCreateSerializer

        return PaymentSerializer

    def list(self, request, *args, **kwargs):
        query_string = request.META.get("QUERY_STRING", "")

        version = cache.get(
            "payment_cache_version",
            1,
        )

        cache_key = f"payment_list_{version}_{query_string}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            cache.set(
                cache_key,
                response.data,
                timeout=60 * 5,
            )

        return response


class PaymentCurdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    queryset = Payment.objects.select_related("member")

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PaymentCreateSerializer

        return PaymentSerializer

    def retrieve(self, request, *args, **kwargs):
        payment_id = kwargs.get("pk")

        version = cache.get(
            "payment_cache_version",
            1,
        )

        cache_key = f"payment_detail_{version}_{payment_id}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            cache.set(
                cache_key,
                response.data,
                timeout=60 * 5,
            )

        return response
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        member = instance.member

        if member.payment_due_date:
            member.payment_due_date = previous_month(
                member.payment_due_date
            )
            member.save(update_fields=["payment_due_date"])

        instance.delete()

        return Response(status=204)


        



def previous_month(date):

    year = date.year
    if date.month == 1:
        month = 12
    else:
            month = date.month - 1

    if month == 12:
        
        year -= 1
    print(month)
    print(year)

    last_day = calendar.monthrange(
        year,
        month
    )[1]
    print(last_day)

   
    day = min(
        date.day,
        last_day
    )
    print(day)

    return date.replace(
        year=year,
        month=month,
        day=day
    )
