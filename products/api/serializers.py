from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.SlugField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=Product.objects.all(), message="SKU already in use!"
            )
        ],
    )

    class Meta:
        model = Product
        fields = ["id", "sku", "name", "description", "active"]


class CsvUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ["file"]
