from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Payment
from .serializer import PaymentSerializer,PaymentCreateSerializer



class PaymentView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser]

    queryset = Payment.objects.select_related('member')
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        else: return PaymentSerializer


class PaymentCurdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[ IsAdminUser]
    queryset = Payment.objects.select_related('member')
    serializer_class = PaymentCreateSerializer

