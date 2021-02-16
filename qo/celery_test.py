import qo
import pytest
from uuid import uuid4
from . import celery


class TestCeleryDistributor:
    @pytest.fixture
    def routine(self):
        @qo.routine(queue="nothing")
        def demo_routine():
            """This routine doesn't do anything."""

        yield demo_routine
        qo.registry.unregister(demo_routine)

    def test_send(self, mocker, routine):
        receive = mocker.patch("qo.celery.receive")
        distributor = celery.CeleryDistributor()
        task = qo.Task(routine=routine)
        distributor.send([task])
        receive.apply_async.assert_called_once_with(
            task_id=str(task.uuid), queue=routine.queue
        )


class TestReceive:
    @pytest.fixture
    def routine(self):
        @qo.routine(queue="nothing")
        def demo_routine():
            """This routine doesn't do anything."""

        yield demo_routine
        qo.registry.unregister(demo_routine)

    def test_qo(self, routine, mocker):
        uuid = uuid4()
        qo_receive = mocker.patch("qo.receive")
        celery.receive.apply(task_id=str(uuid))
        qo_receive.assert_called_once_with(uuid)
