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


class RetrieveUpdateDestroyProductsViewTestCase(TestCase):

    def setUp(self) -> None:
        self.product = ProductFactory.create(
            sku="not-again",
            name="example product 2",
            description="fine test product"
        )

    def test_fetch_single_product(self):
        """Test that a single product can be fetched successfully 
        """
        self.url = reverse(
            "api1:products:retrieve_update_delete_products",
            kwargs={"sku": self.product.sku}
            )
        response = self.client.get(self.url)

        self.assertEqual(response.data["sku"], self.product.sku)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["description"], self.product.description)
        self.assertFalse(response.data["active"], self.product.active)

    def test_delete_product(self):
        """Test that a product can be deleted successfully
        """
        self.url = reverse(
            "api1:products:retrieve_update_delete_products",
            kwargs={"sku": self.product.sku}
            )
        
        response = self.client.delete(self.url)

        self.assertIsNone(response.data)
        self.assertEqual(response.status_code, 204)

    def test_update_product(self):
        """Test that a product can be updated successfully
        """
        self.url = reverse(
            "api1:products:retrieve_update_delete_products",
            kwargs={"sku": self.product.sku}
            )
        new_data = {
            "name": "new name"
        }
        response = self.client.patch(self.url, new_data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], new_data["name"])
        self.assertNotEqual(response.data["name"], self.product.name)
