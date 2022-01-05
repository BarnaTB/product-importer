from collections import defaultdict

from django.apps import apps
from django.db import IntegrityError


class ProductManager(object):

    def __init__(self, batch_size=500):
        self._product_queue = defaultdict(list)
        self.batch_size = batch_size

    def _commit(self, model):
        """
        Private method to commit each batch to the db

        Args:
            model ([type] <Model>): Model whose instances are to be processed
        """
        model_key = model._meta.label
        try:
            model.objects.bulk_create(self._product_queue[model_key])
        except IntegrityError:
            for item in self._product_queue[model_key]:
                defaults = item.__dict__
                del defaults['id']
                del defaults['_state']
                model.objects.update_or_create(sku=item.sku, defaults=defaults)
        self._product_queue[model_key] = []

    def add(self, obj):
        """
        Method to add Product objects to the queue with respect to the batch size

        Args:
            obj ([type] <Model>):
                Model object to be added to the queue for processing
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._product_queue[model_key].append(obj)
        if len(self._product_queue[model_key]) >= self.batch_size:
            self._commit(model_class)


    def done(self):
        """
        Method to process the final batch of objects in the queue.
        """
        for model_name, objs in self._product_queue.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))
