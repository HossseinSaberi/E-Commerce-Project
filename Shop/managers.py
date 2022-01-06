from django.db import models

class SubmittedShopManager(models.Manager):
    print('submited manager')
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class DraftShopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=2)


class DeletedShopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=3)


