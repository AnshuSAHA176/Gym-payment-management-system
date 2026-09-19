from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Payment
from .serializer import PaymentSerializer,PaymentCreateSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend

@method_decorator(
    cache_page(60 * 5, key_prefix='payment_list'),
    name='get'
)
class PaymentView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser]

    queryset = Payment.objects.select_related('member')
    backend_filters = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    
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

