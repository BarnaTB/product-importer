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

progress_list = []


def stream_task_progress(incrementor, maximum):
    """Function to stream the progress of a celery task
    """
    rows_processed = 0
    while True:
        # task_result = TaskResult.objects.get(task_id=task_id)
        # current_state = model_to_dict(task_result)
        if rows_processed == maximum:
            progress_list.clear()
        else:

            # if initial_state == current_state:
            # print(type())
            rows_processed += incrementor
            progress_list.append((rows_processed, maximum))
            print(f"rows processed >>>>>>>>>>> {rows_processed} <<<<<<<<<<<<<<<<<<")
            # yield (rows_processed, maximum)

        # initial_state = json.dumps(current_state)



@shared_task(bind=True)
def upload_products(self, products):
    """Celery task to asynchronously upload a batch of products

    Args:
        products ([type]): [description]
    """
    product_manager = ProductManager(batch_size=1000)
    # progress_recorder = ProgressRecorder(self)
    # count = 0
    number_of_products = len(products)
    def stream_task_progress():
        """Function to stream the progress of a celery task
        """
        rows_processed = 0
        while True:
            # task_result = TaskResult.objects.get(task_id=task_id)
            # current_state = model_to_dict(task_result)
            if rows_processed == number_of_products:
                progress_list.clear()
            else:

                # if initial_state == current_state:
                # print(type())
                rows_processed += incrementor
                progress_list.append((rows_processed, maximum))
                print(f"rows processed >>>>>>>>>>> {rows_processed} <<<<<<<<<<<<<<<<<<")
                yield (rows_processed, maximum)

            # initial_state = json.dumps(current_state)
            # progress_recorder.set_progress(
            #     count + 1,
            #     number_of_products,
            #     f"{count} products processed")
    for row in products:
        product = Product(sku=row[1], name=row[0], description=row[2])
        product_manager.add(product)
        stream_task_progress(1, number_of_products)
    product_manager.done()
