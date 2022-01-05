from django.urls import include, path


urlpatterns = [
    path("products/",
    include(("products.api.urls", "products"), namespace="products"))
]
