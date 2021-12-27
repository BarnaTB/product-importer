from multiprocessing.pool import ThreadPool
import os

from celery.utils.log import get_task_logger

from productimporter import celery_app as app
from products.managers import ProductManager
from products.models import Product


logger = get_task_logger(__name__)


@app.task()
def upload_products(products):
    """Celery task to asynchronously upload a batch of products

    Args:
        products ([type]): [description]
    """
    product_manager = ProductManager(batch_size=1000)
    for row in products:
        product = Product(sku=row[1], name=row[0], description=row[2])
        product_manager.add(product)
    product_manager.done()
