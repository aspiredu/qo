from typing import Iterable, Optional
from abc import ABC, abstractmethod
from uuid import UUID
from .task import Task
from .operation import Operation


class Storage(ABC):
    @abstractmethod
    def write(self, operation: Operation):
        """Write an operation to storage, including tasks and dependencies."""
        raise NotImplementedError

    @abstractmethod
    def read(self, uuid: UUID) -> Optional[Task]:
        """Read a task from storage."""
        raise NotImplementedError

    @abstractmethod
    def stop(self, task: Task) -> Iterable[Task]:
        raise NotImplementedError
