from multiprocessing.pool import ThreadPool
import os

from celery.utils.log import get_task_logger
from celery_progress.backend import Progress, ProgressRecorder

from productimporter import celery_app as app
from products.managers import ProductManager
from products.models import Product


logger = get_task_logger(__name__)


@app.task()
def upload_products(self, products):
    """Celery task to asynchronously upload a batch of products

    Args:
        products ([type]): [description]
    """
    product_manager = ProductManager(batch_size=1000)
    progress_recorder = ProgressRecorder(self)
    count = 0
    number_of_products = len(products)
    for row in products:
        product = Product(sku=row[1], name=row[0], description=row[2])
        product_manager.add(product)
        progress_recorder.set_progress(
            count + 1,
            number_of_products,
            f"{count} products processed")
    product_manager.done()
