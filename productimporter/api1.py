from django.urls import include, path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Product Importer API",
        default_version='v1',
        description="API documentation for  Product Importer",
        contact=openapi.Contact(email="barnabastb2@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("products/",
    include(("products.api.urls", "products"), namespace="products")),
    path("docs/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
