import csv, io

from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.api.serializers import CsvUploadSerializer, ProductSerializer


class ProductView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

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
        # upload_products_csv.delay(decoded_file)
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        
        for row in reader:
            print(row)
        return Response(status=status.HTTP_204_NO_CONTENT)
