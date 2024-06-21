from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.authentication.api.urls')),
    path("", include("apps.openapi.urls")),
]
