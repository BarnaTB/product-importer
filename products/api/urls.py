from django.urls import path

from products.api.views import ProductView, CsvUploadView, RetrieveUpdateDestroyProductsView


urlpatterns = [
    path("", ProductView.as_view(), name="create_list_products"),
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
    path("<str:sku>/", RetrieveUpdateDestroyProductsView.as_view(), name="retrieve_update_delete_products")
]
