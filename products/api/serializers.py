from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django_celery_results.models import TaskResult

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


class TaskResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = "__all__"
