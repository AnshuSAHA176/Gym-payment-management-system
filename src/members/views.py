
from rest_framework import viewsets

from .models import Member
from rest_framework.permissions import IsAdminUser
from .serializer import MemberSerializer,MemberDashboardSerializer,OverDueSerializer
from rest_framework import filters
from rest_framework import generics

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination




class MemberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50



@method_decorator(
    cache_page(60 * 5, key_prefix="member_list"),
    name="list"
)
class MemeberViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name', 'phone',"member_id"]
    pagination_class=MemberPagination
    filterset_fields = ['is_active']


# NEW 
@method_decorator(
    cache_page(60 * 15, key_prefix='overdue_members'),
    name='get'
)
class OverDeuMembers(generics.ListAPIView):

    serializer_class = OverDueSerializer
    permission_classes = [IsAdminUser]
    filter_backends=[filters.SearchFilter]
    search_fields = ['name', 'phone',"member_id"]

    def get_queryset(self):
        return Member.objects.filter(payment_due_date__lt=timezone.localdate())