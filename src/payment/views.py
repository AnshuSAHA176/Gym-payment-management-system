from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend

from .models import Payment
from .serializer import PaymentSerializer, PaymentCreateSerializer
from .filters import PaymentFilter


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
        cache_key = "payment_list"

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
        cache_key = f"payment_detail_{payment_id}"

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