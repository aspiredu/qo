from .routine import Routine


class Registry:
    """A mapping of registered callables."""

    def __init__(self):
        self.__registry = {}

    def register(self, routine: Routine):
        """Register a task to a name."""
        self.__registry[routine.name] = routine

    def routine(self, name: str):
        """Get the routine for the given name."""
        return self.__registry[name]

    def unregister(self, routine: Routine):
        """Remove the routine from the registry."""
        self.__registry.pop(routine.name)
