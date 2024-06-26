from __future__ import annotations

import base64
import importlib
import json
import uuid
from typing import Any

from eb_sqs import settings


class WorkerTask:
    def __init__(
        self,
        id: str,  # noqa: A002
        group_id: str | None,
        queue: str,
        func: Any,
        args: tuple,
        kwargs: dict,
        max_retries: int,
        retry: int,
        retry_id: str | None,
    ) -> None:
        super().__init__()
        self.id = id
        self.group_id = group_id
        self.queue = queue
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.max_retries = max_retries
        self.retry = retry
        self.retry_id = retry_id

        self.abs_func_name = f"{self.func.__module__}.{self.func.__name__}"

    def execute(self) -> Any:
        from eb_sqs.decorators import func_retry_decorator

        self.func.retry_num = self.retry
        self.func.retry = func_retry_decorator(worker_task=self)
        return self.func(*self.args, **self.kwargs)

    def serialize(self) -> str:
        args = self.args
        kwargs = self.kwargs

        task = {
            "id": self.id,
            "groupId": self.group_id,
            "queue": self.queue,
            "func": self.abs_func_name,
            "args": args,
            "kwargs": kwargs,
            "maxRetries": self.max_retries,
            "retry": self.retry,
            "retryId": self.retry_id,
        }

        return json.dumps(task)

    def copy(self, use_serialization: bool) -> WorkerTask:
        if use_serialization:
            return WorkerTask.deserialize(self.serialize())
        else:
            return WorkerTask(
                self.id,
                self.group_id,
                self.queue,
                self.func,
                self.args,
                self.kwargs,
                self.max_retries,
                self.retry,
                self.retry_id,
            )

    @staticmethod
    def deserialize(msg: str) -> WorkerTask:
        task = json.loads(msg)

        id = task.get("id", str(uuid.uuid4()))  # noqa: A001
        group_id = task.get("groupId")

        abs_func_name = task["func"]
        func_name = abs_func_name.split(".")[-1]
        func_path = ".".join(abs_func_name.split(".")[:-1])
        func_module = importlib.import_module(func_path)

        func = getattr(func_module, func_name)

        queue = task.get("queue", settings.DEFAULT_QUEUE)

        task_args = task.get("args", [])
        args = task_args

        kwargs = task["kwargs"]

        max_retries = task.get("maxRetries", settings.DEFAULT_MAX_RETRIES)
        retry = task.get("retry", 0)
        retry_id = task.get("retryId")

        return WorkerTask(
            id,
            group_id,
            queue,
            func,
            args,
            kwargs,
            max_retries,
            retry,
            retry_id,
        )
