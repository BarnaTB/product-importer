from django.urls import path

from products.api.views import ProductView, CsvUploadView, RetrieveUpdateDestroyProductsView


urlpatterns = [
    path("", ProductView.as_view(), name="products"),
    path("upload/", CsvUploadView.as_view(), name="products"),
    path("products/", RetrieveUpdateDestroyProductsView.as_view(), name="products")
]
