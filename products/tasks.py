import json

from multiprocessing.pool import ThreadPool
import os
from time import time

from celery.utils.log import get_task_logger
from celery import shared_task
from django_celery_results.models import TaskResult

from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
# from celery_progress.backend import Progress, ProgressRecorder

from products.managers import ProductManager
from products.models import Product


logger = get_task_logger(__name__)


def stream_task_progress(task_id):
    """Function to stream the progress of a celery task
    """
    initial_state = {}
    while True:
        task_result = TaskResult.objects.get(task_id=task_id)
        current_state = task_result.as_dict()

        if not initial_state == current_state:
            yield current_state



@shared_task(bind=True)
def upload_products(self, products):
    """Celery task to asynchronously upload a batch of products

    Args:
        products ([type]): [description]
    """
    product_manager = ProductManager(batch_size=1000)
    for row in products:
        product = Product(sku=row[1], name=row[0], description=row[2])
        product_manager.add(product)
    product_manager.done()
