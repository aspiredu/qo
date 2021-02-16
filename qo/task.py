from typing import List, Dict, Any
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .routine import Routine


@dataclass(frozen=True)
class Task:
    """A signature for a qo task."""

    routine: Routine = field(compare=False)
    args: List[Any] = field(default_factory=list, compare=False)
    kwargs: Dict[str, Any] = field(default_factory=dict, compare=False)
    uuid: UUID = field(default_factory=uuid4, compare=True)
