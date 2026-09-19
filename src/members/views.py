from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination

from django.core.cache import cache
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Member
from .serializer import (
    MemberSerializer,
    MemberDashboardSerializer,
    OverDueSerializer,
)


class MemberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50


class MemeberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by("name")
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        "name",
        "phone",
        "member_id",
    ]

    pagination_class = MemberPagination
    filterset_fields = ["is_active"]

    def list(self, request, *args, **kwargs):
        """
        Return cached member list when available.
        """

        # Create a unique cache key based on query parameters
        query_string = request.META.get("QUERY_STRING", "")
        cache_key = f"member_list"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        # Generate normal DRF response
        response = super().list(request, *args, **kwargs)

        # Cache only successful responses
        if response.status_code == 200:
            cache.set(
                cache_key,
                response.data,
                timeout=60 * 5,
            )

        return response


class OverDeuMembers(generics.ListAPIView):
    serializer_class = OverDueSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        "name",
        "phone",
        "member_id",
    ]

    def get_queryset(self):
        return Member.objects.filter(
            payment_due_date__lt=timezone.localdate()
        )

    def list(self, request, *args, **kwargs):
        """
        Return cached overdue-member list when available.
        """

        query_string = request.META.get("QUERY_STRING", "")
        cache_key = f"overdue_members"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            cache.set(
                cache_key,
                response.data,
                timeout=60 * 15,
            )

        return response