from typing import Iterable, Optional
from collections import defaultdict, deque
from uuid import UUID

from qo.task import Task
from qo.operation import Operation
from qo.distributor import Distributor
from qo.storage import Storage
from qo import receive


class StubDistributor(Distributor):
    def __init__(self):
        self.queues = defaultdict(deque)

    def send(self, tasks: Iterable[Task]):
        for task in tasks:
            self.queues[task.routine.queue].append(task.uuid)

    def process(self, *, queue: str):
        """Process the tasks on the named queue."""
        while self.queues[queue]:
            receive(self.queues[queue].popleft())


class StubStorage(Storage):
    def __init__(self):
        self.tasks = {}
        self.dependencies = defaultdict(set)

    def write(self, operation: Operation):
        """Write an operation to storage, including tasks and dependencies."""
        self.tasks.update({task.uuid: task for task in operation.tasks})
        for dependent, dependency in operation.dependencies:
            self.dependencies[dependent].add(dependency)

    def read(self, uuid: UUID) -> Optional[Task]:
        """Read the task from storage."""
        return self.tasks.get(uuid)

    def stop(self, task: Task) -> Iterable[Task]:
        """Mark the task as completed, and find ready tasks, atomically."""
        self.tasks.pop(task.uuid)
        dependents = [
            dependent
            for dependent in self.dependencies
            if task in self.dependencies[dependent]
        ]
        for dependent in dependents:
            self.dependencies[dependent].remove(task)
            if not self.dependencies[dependent]:
                self.dependencies.pop(dependent)
                yield dependent
