from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Payment
from .serializer import PaymentSerializer,PaymentCreateSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
class PaymentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50




@method_decorator(
    cache_page(60 * 5, key_prefix='payment_list'),
    name='get'
)
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

@method_decorator(
    cache_page(60 * 5, key_prefix='payment_detail'),
    name='get'
)
class PaymentCurdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[ IsAdminUser]
    queryset = Payment.objects.select_related('member')
    serializer_class = PaymentCreateSerializer

