# Generated by Django 3.1.2 on 2020-10-27 16:11

from django.db import migrations, models
import django.db.models.deletion
import uuid
from django_safemigrate import Safe


class Migration(migrations.Migration):
    safe = Safe.before_deploy

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Operation",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("uuid", models.UUIDField(primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "routine",
                    models.CharField(
                        help_text="The name of the registered routine.", max_length=256
                    ),
                ),
                ("args", models.JSONField(help_text="The positional arguments.")),
                ("kwargs", models.JSONField(help_text="The keyword arguments.")),
                (
                    "operation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="qo.operation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskDependency",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dependency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_dependents",
                        to="qo.task",
                    ),
                ),
                (
                    "dependent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_dependencies",
                        to="qo.task",
                    ),
                ),
            ],
            options={
                "unique_together": {("dependent", "dependency")},
            },
        ),
    ]