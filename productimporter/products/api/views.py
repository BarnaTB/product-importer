import csv, io

from django.shortcuts import render
from django.conf import settings

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.tasks import upload_products
from products.api.serializers import CsvUploadSerializer, ProductSerializer
from products.models import Product


class ProductView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        """Method to create a new product manually

        Args:
            request ([type]): [description]

        Returns:
            dict: Dictionary containing a success status and message
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "success": True,
            "message": "Product created successfully!"
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CsvUploadView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CsvUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        # print(dir(reader))
        # print("reader length >>>>>>>>>>>>>>>>>>>>>> ", dir(reader))
        # rows = list(reader)
        next(reader)
        # print(len(reader))
        # for row in reader:
        #     print(row)
        # print(list(reader))
        # upload_products_csv.chunks(reader, settings.CELERY_CHUNK_SIZE).apply_sync(queue="high_priority")
        task_id = upload_products.delay(list(reader))
        print(">>>>>>>>>>>>>>>>>>>>>>> ", task_id)
        # product_chunks.apply_async(queue="high_priority")

        response_data = {
            "success": True,
            "message": "Products created successfully!"
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyProductsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        Product.objects.all().delete()

        response_data = {
            "success": True,
            "message": "All products deleted successfully!"
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
