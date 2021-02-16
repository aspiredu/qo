from uuid import uuid4
from .admin import OperationAdmin, TaskAdmin, Operation, Task
import pytest


class TestOperationAdmin:
    @pytest.mark.django_db
    def test_tasks_count(self, rf):
        request = rf.get("/")
        admin = OperationAdmin(Operation, None)
        Operation.objects.create()
        assert admin.tasks(list(admin.get_queryset(request))[0]) == 0


class TestTaskAdmin:
    @pytest.mark.django_db
    def test_dependencies_count(self, rf):
        request = rf.get("/")
        admin = TaskAdmin(Task, None)
        Task.objects.create(
            uuid=uuid4(),
            operation=Operation.objects.create(),
            routine="routine",
            args=[],
            kwargs={},
        )
        assert admin.dependencies(list(admin.get_queryset(request))[0]) == 0
