from .django import DjangoStorage
import qo
import pytest
from uuid import uuid4


class TestDjangoStorage:
    @pytest.fixture
    def routine(self):
        @qo.routine(queue="routine")
        def routine():
            pass

        yield routine
        qo.registry.unregister(routine)

    @pytest.fixture
    def storage(self):
        return DjangoStorage()

    @pytest.mark.django_db
    def test_store_task(self, routine, storage):
        task = qo.Task(routine=routine)
        storage.write(qo.Operation(tasks={task}))
        assert storage.read(task.uuid) == task
        assert storage.read(uuid4()) is None

    @pytest.mark.django_db
    def test_store_dependencies(self, routine, storage):
        dependent = qo.Task(routine=routine)
        dependency = qo.Task(routine=routine)
        operation = qo.Operation(
            tasks={dependent, dependency}, dependencies={(dependent, dependency)}
        )
        storage.write(operation)
        assert set(storage.stop(dependency)) == {dependent}
