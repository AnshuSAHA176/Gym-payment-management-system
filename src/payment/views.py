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

class PaymentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50




@method_decorator(
    cache_page(60 * 5, key_prefix='payment_list'),
    name='get'
)
class PaymentView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser]

    queryset = Payment.objects.select_related('member')
    backend_filters = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    pagination_class =PaymentPagination
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        else: return PaymentSerializer

@method_decorator(
    cache_page(60 * 5, key_prefix='payment_detail'),
    name='get'
)
class PaymentCurdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[ IsAdminUser]
    queryset = Payment.objects.select_related('member')
    serializer_class = PaymentCreateSerializer

