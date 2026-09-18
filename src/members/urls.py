from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MemeberViewSet, OverDeuMembers


router = DefaultRouter()

router.register(
    "",
    MemeberViewSet,
    basename="member",
)

urlpatterns = [
    path(
        "overdue/",
        OverDeuMembers.as_view(),
        name="over-due",
    ),
]

urlpatterns += router.urls