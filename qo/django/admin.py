from django.contrib import admin
from django.db.models import Count
from .models import Operation, Task


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ["uuid", "created", "tasks"]
    readonly_fields = ["uuid", "created"]
    list_filter = ["created"]
    search_fields = ["uuid"]

    def tasks(self, obj):
        return obj.tasks_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(tasks_count=Count("tasks"))


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["uuid", "created", "routine", "dependencies"]
    readonly_fields = ["uuid", "operation", "routine", "args", "kwargs", "created"]
    list_filter = ["created", "routine"]
    search_fields = ["uuid", "operation__uuid", "routine"]

    def dependencies(self, obj):
        return obj.task_dependencies_count

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(task_dependencies_count=Count("task_dependencies"))
        )
