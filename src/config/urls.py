

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("members/", include("members.urls")),
    path("payment/", include("payment.urls")),
    path("agent/", include("agent.urls")),
]
