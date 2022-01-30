import csv, io
from urllib import response

from django.shortcuts import render
from django.conf import settings
from django.http import StreamingHttpResponse

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from productimporter.utils.decorators import required_fields
from productimporter.utils.exceptions import CustomAPIException
from productimporter.settings_utils import get_env_variable

from products.tasks import stream_task_progress, upload_products
from products.api.serializers import CsvUploadSerializer, ProductSerializer
from products.models import Product


class ProductView(mixins.DestroyModelMixin, generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        """Method to create a new product manually

        Args:
            request ([HttpRequest]): HttpRequest sent to the server

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

    def delete(self, request, *args, **kwargs):
        """Method to delete all products

        Args:
            request ([HttpRequest]): HttpRequest sent to the server
            Returns:
            dict: Dictionary containing a success message
        """
        self.queryset.delete()

        response_data = {
            "detail": "You deleted all products!"
        }

        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)


class CsvUploadView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CsvUploadSerializer

    def post(self, request, *args, **kwargs):
        """Method to upload a csv of products
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        next(reader)
        task = upload_products.delay(list(reader))

        response_data = {
            "success": True,
            "task_id": task.task_id,
            "message": "Products created successfully!"
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class TaskProgressStreamView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    @required_fields(["task_id"])
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        print(task_id)
        print(type(task_id))
        response = StreamingHttpResponse(
            streaming_content=stream_task_progress(task_id),
            )
        response.headers["Content-Type"] = "text/event-stream"
        response.headers["Access-Control-Allow-Origin"] = get_env_variable("CORS_ORIGIN_WHITELIST", required=True)

        return response


class RetrieveUpdateDestroyProductsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    lookup_url_kwargs = "sku"
    lookup_field = "sku"
    queryset = Product.objects.all()
