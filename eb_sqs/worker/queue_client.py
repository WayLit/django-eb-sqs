from __future__ import annotations

from abc import ABCMeta, abstractmethod


class QueueClientException(Exception):  # noqa: N818
    pass


class QueueDoesNotExistException(QueueClientException):
    def __init__(self, queue_name: str) -> None:
        super().__init__()
        self.queue_name = queue_name


class QueueClient(metaclass=ABCMeta):
    @abstractmethod
    def add_message(self, queue_name: str, msg: str, delay: int) -> None:
        pass
