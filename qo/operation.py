from typing import Tuple, Set
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .task import Task


@dataclass(frozen=True)
class Operation:
    """A collection of tasks and associated dependencies."""

    tasks: Set[Task] = field(compare=False)
    dependencies: Set[Tuple[Task, Task]] = field(default_factory=set, compare=False)
    uuid: UUID = field(default_factory=uuid4, compare=True)

    def ready(self) -> Set[Task]:
        """Find the tasks that do not depend on other tasks."""
        return self.tasks - {dependent for dependent, _ in self.dependencies}
