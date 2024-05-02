from __future__ import annotations

from eb_sqs.aws.sqs_queue_client import SqsQueueClient
from eb_sqs.worker.worker import Worker
from eb_sqs.worker.worker_factory import WorkerFactory


class SqsWorkerFactory(WorkerFactory):
    _WORKER: Worker | None = None

    def __init__(self) -> None:
        super().__init__()

    def create(self) -> Worker:
        if not SqsWorkerFactory._WORKER:
            SqsWorkerFactory._WORKER = Worker(SqsQueueClient())
        return SqsWorkerFactory._WORKER
