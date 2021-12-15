from django.urls import path

from products.api.views import ProductView


urlpatterns = [
    path("", ProductView.as_view(), name="products")
]
