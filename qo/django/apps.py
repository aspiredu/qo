from django.apps import AppConfig


class QoConfig(AppConfig):
    name = "qo.django"
    label = "qo"

    def ready(self):
        import qo
        from qo.django import DjangoStorage
        from qo.celery import CeleryDistributor

        qo.distributor = CeleryDistributor()
        qo.storage = DjangoStorage()
