from django.urls import path

from products.api.views import ProductView, CsvUploadView, RetrieveUpdateDestroyProductsView, TaskProgressStreamView


urlpatterns = [
    path("", ProductView.as_view(), name="create_list_products"),
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
    path("product/<str:sku>/", RetrieveUpdateDestroyProductsView.as_view(), name="retrieve_update_delete_products"),
    path("stream/<uuid:task_id>/", TaskProgressStreamView.as_view(), name="stream")
]
