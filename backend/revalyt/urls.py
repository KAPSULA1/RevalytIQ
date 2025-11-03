from django.contrib import admin
from django.urls import path, include

from .health import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/analytics/", include("analytics.urls")),
    path("api/auth/", include("users.urls")),
    path("health/", health, name="health"),
]
