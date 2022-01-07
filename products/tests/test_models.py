from django.test import TestCase
from products.models import Product

from products.tests.factories import ProductFactory


class ProductModelTestCase(TestCase):

    def test_create_product(self):
        """
        Test that the Product model instance successfully creates a product
        """
        product = ProductFactory.create(
            sku="test-product-sku",
            name="test product name",
            description="test product description"
            )

        self.assertIsInstance(product, Product)
        self.assertEqual(product.sku, "test-product-sku")
        self.assertEqual(product.name, "test product name")
        self.assertEqual(product.description, "test product description")
