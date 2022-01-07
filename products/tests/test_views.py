from django.test.testcases import TestCase
from django.urls import reverse
from django.test import SimpleTestCase

from products.tests.factories import ProductFactory


class ProductViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse("api1:products:create_list_products")
        self.product = ProductFactory()

    def test_create_product(self):
        """Test that a product can be created successfully
        """
        payload = {
            "sku": "not-again",
            "name": "example product 2",
            "description": "fine test product"
        }

        response = self.client.post(self.url, data=payload)


        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data["message"], "Product created successfully!")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_fetch_products(self):
        """Test that products can be fetched successfully
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
