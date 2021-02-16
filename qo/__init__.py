from typing import Callable, Optional, Iterable
from uuid import UUID
from .registry import Registry
from .routine import Routine, Continue
from .task import Task
from .operation import Operation
from .storage import Storage
from .distributor import Distributor


registry: Registry = Registry()
storage: Optional[Storage] = None
distributor: Optional[Distributor] = None


def routine(
    *, queue: str, name: Optional[str] = None
) -> Callable[[Callable[..., Optional[Continue]]], Routine]:
    def wrapper(fn):
        routine = Routine(fn, name=name or fn.__name__, queue=queue)
        registry.register(routine)
        return routine

    return wrapper


def receive(uuid: UUID):
    if not storage:
        raise RuntimeError("qo storage is not configured.")
    if not distributor:
        raise RuntimeError("qo distributor is not configured.")

    task = storage.read(uuid)
    if task:
        signal = task.routine(*task.args, **task.kwargs)
        ready: Iterable[Task]
        if signal:
            ready = [task]
        else:
            ready = storage.stop(task)
        distributor.send(ready)


def send(operation: Operation):
    if not storage:
        raise RuntimeError("qo storage is not configured.")
    storage.write(operation)

    if not distributor:
        raise RuntimeError("qo distributor is not configured.")
    distributor.send(operation.ready())
