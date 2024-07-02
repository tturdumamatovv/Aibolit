from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.medicine.api.views import admin_change_category

urlpatterns = [
    path("admin/change_category/", admin_change_category, name="admin_change_category"),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.authentication.api.urls')),
    path('api/v1/', include('apps.medicine.api.urls')),
    path('api/v1/', include('apps.order.api.urls')),
    path('api/v1/', include('apps.pages.api.urls')),
    path("", include("apps.openapi.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
