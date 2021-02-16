"""Abstract interfaces for a task runner.

A task runner takes tasks and distributes them to worker processes to run.
The worker processes will then call a public function to process the task.
"""
from typing import Iterable
from abc import ABC, abstractmethod
from .task import Task


class Distributor(ABC):
    @abstractmethod
    def send(self, tasks: Iterable[Task]):
        """Send the given task to a worker to be run.

        How it is sent and where is an implementation detail.
        """
        raise NotImplementedError
