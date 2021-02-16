from uuid import UUID
from .models import Operation, Task, TaskDependency
import pytest


class TestOperation:
    @pytest.mark.django_db
    def test_repr(self):
        operation = Operation.objects.create(
            uuid=UUID("eac0e8d5-c110-4ae9-afa4-f80111bb3fa5")
        )
        assert "Operation" in repr(operation)
        assert "eac0e8d5-c110-4ae9-afa4-f80111bb3fa5" in repr(operation)

    @pytest.mark.django_db
    def test_str(self):
        operation = Operation.objects.create(
            uuid=UUID("1d107500-ca7e-4c6d-a773-a6428e4a71d5")
        )
        assert str(operation) == "1d107500-ca7e-4c6d-a773-a6428e4a71d5"


class TestTask:
    @pytest.mark.django_db
    def test_repr(self):
        task = Task.objects.create(
            operation=Operation.objects.create(),
            uuid=UUID("7e18b999-75a2-4d5d-95ea-cfa51717b5eb"),
            routine="routine",
            args=[],
            kwargs={},
        )
        assert "Task" in repr(task)
        assert "7e18b999-75a2-4d5d-95ea-cfa51717b5eb" in repr(task)

    @pytest.mark.django_db
    def test_str(self):
        task = Task.objects.create(
            operation=Operation.objects.create(),
            uuid=UUID("bfeb01d1-2350-4044-a955-0e2946b7593f"),
            routine="routine",
            args=[],
            kwargs={},
        )
        assert str(task) == "bfeb01d1-2350-4044-a955-0e2946b7593f"


class TestTaskDependency:
    @pytest.mark.django_db
    def test_repr(self):
        operation = Operation.objects.create()
        dep = TaskDependency.objects.create(
            dependent=Task.objects.create(
                operation=operation,
                uuid=UUID("f8bff033-90ee-4729-b7a8-cd41308a1b93"),
                routine="dependent",
                args=[],
                kwargs={},
            ),
            dependency=Task.objects.create(
                operation=operation,
                uuid=UUID("8d18fdec-e4c7-453f-bcb5-284f003d9456"),
                routine="dependent",
                args=[],
                kwargs={},
            ),
        )
        assert "TaskDependency" in repr(dep)
        assert "f8bff033-90ee-4729-b7a8-cd41308a1b93" in repr(dep)
        assert "8d18fdec-e4c7-453f-bcb5-284f003d9456" in repr(dep)
        dependent_index = repr(dep).index("f8bff033-90ee-4729-b7a8-cd41308a1b93")
        dependency_index = repr(dep).index("8d18fdec-e4c7-453f-bcb5-284f003d9456")
        assert dependent_index < dependency_index  # dependent should come first
