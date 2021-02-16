from .registry import Registry
from .routine import Routine
import pytest


class TestRegistry:
    def test_register(self):
        routine = Routine(lambda: None, name="routine", queue="queue")
        registry = Registry()
        with pytest.raises(KeyError):
            registry.routine("routine")
        registry.register(routine)
        assert registry.routine("routine") == routine

    def test_unregister(self):
        routine = Routine(lambda: None, name="routine", queue="queue")
        registry = Registry()
        with pytest.raises(KeyError):
            registry.routine("routine")
        registry.register(routine)
        assert registry.routine("routine") == routine
        registry.unregister(routine)
        with pytest.raises(KeyError):
            registry.routine("routine")
