
from rest_framework import viewsets

from .models import Member
from rest_framework.permissions import IsAdminUser
from .serializer import MemberSerializer
from rest_framework import filters
from rest_framework import generics
from .serializer import MemberDashboardSerializer
from django.utils import timezone


class MemeberViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]
    filter_backends=[filters.SearchFilter]
    search_fields = ['name', 'phone',"member_id"]


# NEW 

class OverDeuMembers(generics.ListAPIView):

    serializer_class = MemberDashboardSerializer
    permission_classes = [IsAdminUser]
    filter_backends=[filters.SearchFilter]
    search_fields = ['name', 'phone',"member_id"]

    def get_queryset(self):
        return Member.objects.filter(payment_due_date__lt=timezone.localdate())