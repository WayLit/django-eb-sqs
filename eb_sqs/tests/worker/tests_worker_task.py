import json
from unittest import TestCase

from eb_sqs.worker.worker_task import WorkerTask


class TestObject:
    def __init__(self) -> None:
        super().__init__()
        self.message = "Test"


def dummy_function():
    pass


class WorkerTaskTest(TestCase):
    def setUp(self):
        self.dummy_msg = '{"queue": "default", "retryId": "retry-uuid", "retry": 0, "func": "eb_sqs.tests.worker.tests_worker_task.dummy_function", "kwargs": {}, "maxRetries": 5, "args": [], "id": "id-1", "groupId": "group-5"}'

    def test_serialize_worker_task(self):
        worker_task = WorkerTask(
            "id-1", "group-5", "default", dummy_function, (), {}, 5, 0, "retry-uuid"
        )
        msg = worker_task.serialize()

        self.assertDictEqual(json.loads(msg), json.loads(self.dummy_msg))

    def test_deserialize_worker_task(self):
        worker_task = WorkerTask.deserialize(self.dummy_msg)

        self.assertEqual(worker_task.id, "id-1")
        self.assertEqual(worker_task.group_id, "group-5")
        self.assertEqual(worker_task.queue, "default")
        self.assertEqual(worker_task.func, dummy_function)
        self.assertEqual(worker_task.args, [])
        self.assertEqual(worker_task.kwargs, {})
        self.assertEqual(worker_task.max_retries, 5)
        self.assertEqual(worker_task.retry, 0)
        self.assertEqual(worker_task.retry_id, "retry-uuid")
