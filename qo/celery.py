from typing import Iterable
from uuid import UUID
from celery import shared_task
from qo.distributor import Distributor
from qo.task import Task
import qo


class CeleryDistributor(Distributor):
    def send(self, tasks: Iterable[Task]):
        for task in tasks:
            receive.apply_async(task_id=str(task.uuid), queue=task.routine.queue)


@shared_task(name="qo", acks_late=True, bind=True)
def receive(self):
    qo.receive(UUID(self.request.id))
