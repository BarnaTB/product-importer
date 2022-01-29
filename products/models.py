from django.db import models


class TimestampMixin(models.Model):
    """
    Model mixin that provides timestamping fields.
    """

    create_date = models.DateTimeField("date created", auto_now_add=True)
    modify_date = models.DateTimeField("date modified", auto_now=True)

    class Meta:
        abstract = True


class Product(TimestampMixin):
    sku = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.sku}, {self.name}, Active: {self.active}"
