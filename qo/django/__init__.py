from typing import Iterable, Optional
from uuid import UUID
from qo import Task, Operation
from qo.storage import Storage


class DjangoStorage(Storage):
    def write(self, operation: Operation):
        """Write an operation to storage, including tasks and dependencies."""
        from . import models

        written_operation = models.Operation.objects.create(uuid=operation.uuid)
        models.Task.objects.bulk_create(
            models.Task(
                operation=written_operation,
                routine=task.routine.name,
                args=task.args,
                kwargs=task.kwargs,
                uuid=task.uuid,
            )
            for task in operation.tasks
        )
        models.TaskDependency.objects.bulk_create(
            models.TaskDependency(
                dependent_id=dependent.uuid, dependency_id=dependency.uuid
            )
            for dependent, dependency in operation.dependencies
        )

    def read(self, uuid: UUID) -> Optional[Task]:
        """Read the task from storage."""
        from qo import registry
        from . import models

        def translate(task) -> Task:
            return Task(
                routine=registry.routine(task.routine),
                args=task.args,
                kwargs=task.kwargs,
                uuid=task.uuid,
            )

        task = models.Task.objects.filter(uuid=uuid).first()
        return task and translate(task)

    def stop(self, task: Task) -> Iterable[Task]:
        """Mark the task as completed, and find ready tasks, atomically."""
        from django.db import transaction
        from qo import registry
        from . import models

        def translate(task) -> Task:
            return Task(
                routine=registry.routine(task.routine),
                args=task.args,
                kwargs=task.kwargs,
                uuid=task.uuid,
            )

        with transaction.atomic():
            instance = models.Task.objects.select_for_update().get(uuid=task.uuid)
            dependents = list(
                models.Task.objects.select_for_update()
                .filter(task_dependencies__dependency=instance)
                .values_list("uuid", flat=True)
            )
            instance.delete()
            ready = models.Task.objects.filter(
                uuid__in=dependents, task_dependencies__isnull=True
            )
            return {translate(task) for task in ready}
