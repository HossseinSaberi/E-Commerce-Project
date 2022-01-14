from django.db import models

class SubmitOrders(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 1)


class PaidOrders(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 4)


class DraftOrders(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 3)