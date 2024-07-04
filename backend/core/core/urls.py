from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", include("account.urls"), name="users"),
    path("", include("museum.urls"), name="users"),
    path("", include("collection.urls"), name="collections"),
    path("", include("messenger.urls"), name="messenger"),
    path("", include("constructor.urls"), name="constructor"),
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
