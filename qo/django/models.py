from uuid import uuid4
from django.db import models


class Operation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    created = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"<Operation {self.uuid}>"

    def __str__(self):
        return str(self.uuid)


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="tasks"
    )
    routine = models.CharField(
        max_length=256, help_text="The name of the registered routine."
    )
    args = models.JSONField(help_text="The positional arguments.")
    kwargs = models.JSONField(help_text="The keyword arguments.")

    def __repr__(self):
        return f"<Task {self.uuid}>"

    def __str__(self):
        return str(self.uuid)


class TaskDependency(models.Model):
    dependent = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_dependencies",
    )
    dependency = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_dependents",
    )

    class Meta:
        unique_together = ["dependent", "dependency"]

    def __repr__(self):
        return f"<TaskDependency {self.dependent_id} <- {self.dependency_id}"
