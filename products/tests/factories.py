import factory
from faker import Factory

from products.models import Product


faker = Factory.create()


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory class to create test products
    """
    class Meta:
        model = Product
