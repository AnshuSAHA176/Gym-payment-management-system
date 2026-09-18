
from rest_framework import viewsets

from .models import Member
from rest_framework.permissions import IsAdminUser
from .serializer import MemberSerializer



class MemeberViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]