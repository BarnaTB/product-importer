from collections import defaultdict
from django.apps import apps


class BulkCreateManager(object):

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        try:
            model_class.objects.bulk_create(self._create_queues[model_key])
        except Exception:
            for item in self._create_queues[model_key]:
                defaults = item.__dict__
                del defaults['id']
                del defaults['_state']
                model_class.objects.update_or_create(sku=item.sku, defaults=defaults)
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)


    def done(self):
        """
        Call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))
