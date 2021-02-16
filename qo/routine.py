class Routine:
    def __init__(self, fn, *, name: str, queue: str):
        self.__fn = fn
        self.name = name
        self.queue = queue

    def __call__(self, *args, **kwargs):
        return self.__fn(*args, **kwargs)

    def __repr__(self):
        return f"<{type(self).__name__} {self.name!r}>"


class Continue:
    """Signal that the task should be requeued and re-run."""
