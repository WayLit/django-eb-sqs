from __future__ import annotations


class WorkerException(Exception):  # noqa: N818
    pass


class InvalidMessageFormatException(WorkerException):
    def __init__(self, msg: str, caught: Exception) -> None:
        super().__init__()
        self.msg = msg
        self.caught = caught


class ExecutionFailedException(WorkerException):
    def __init__(self, task_name: str, caught: Exception) -> None:
        super().__init__()
        self.task_name = task_name
        self.caught = caught


class MaxRetriesReachedException(WorkerException):
    def __init__(self, retries: int) -> None:
        super().__init__()
        self.retries = retries


class QueueException(WorkerException):
    pass


class InvalidQueueException(QueueException):
    def __init__(self, queue_name: str) -> None:
        super().__init__()
        self.queue_name = queue_name
