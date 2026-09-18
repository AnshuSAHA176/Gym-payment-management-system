
from rest_framework import viewsets

from .models import Member
from rest_framework.permissions import IsAdminUser
from .serializer import MemberSerializer
from rest_framework import filters



class MemeberViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]
    filter_backends=[filters.SearchFilter]
    search_fields = ['name', 'phone',"member_id"]