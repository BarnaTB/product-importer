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
    active = serializers.BooleanField(read_only=False)

    class Meta:
        model = Product
        fields = ["sku", "name", "description", "active"]
