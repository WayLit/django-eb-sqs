from __future__ import annotations

from typing import Any, Callable

from typing_extensions import ParamSpec

from eb_sqs import settings
from eb_sqs.worker.worker_factory import WorkerFactory
from eb_sqs.worker.worker_task import WorkerTask


def _get_kwarg_val(kwargs: dict, key: str, default: Any) -> Any:
    return kwargs.pop(key, default) if kwargs else default


PS = ParamSpec("PS")


def func_delay_decorator(
    func: Callable[PS, Any], queue_name: str | None, max_retries_count: int | None
) -> Callable[PS, Any]:
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> Any:
        queue = _get_kwarg_val(
            kwargs, "queue_name", queue_name if queue_name else settings.DEFAULT_QUEUE
        )
        max_retries = _get_kwarg_val(
            kwargs,
            "max_retries",
            max_retries_count if max_retries_count else settings.DEFAULT_MAX_RETRIES,
        )

        execute_inline = (
            _get_kwarg_val(kwargs, "execute_inline", False) or settings.EXECUTE_INLINE
        )
        delay = _get_kwarg_val(kwargs, "delay", settings.DEFAULT_DELAY)
        group_id = _get_kwarg_val(kwargs, "group_id", None)

        worker = WorkerFactory.default().create()
        return worker.delay(
            group_id,
            queue,
            func,
            args,
            kwargs,
            max_retries,
            delay,
            execute_inline,
        )

    return wrapper


def func_retry_decorator(worker_task: WorkerTask) -> Callable[..., Any]:
    def wrapper(*args, **kwargs) -> Any:
        execute_inline = (
            _get_kwarg_val(kwargs, "execute_inline", False) or settings.EXECUTE_INLINE
        )
        delay = _get_kwarg_val(kwargs, "delay", settings.DEFAULT_DELAY)
        count_retries = _get_kwarg_val(
            kwargs, "count_retries", settings.DEFAULT_COUNT_RETRIES
        )

        worker = WorkerFactory.default().create()
        return worker.retry(worker_task, delay, execute_inline, count_retries)

    return wrapper


class task:  # noqa: N801
    def __init__(
        self,
        queue_name: str | None = None,
        max_retries: int | None = None,
    ) -> None:
        self.queue_name = queue_name
        self.max_retries = max_retries

    def __call__(self, func: Callable[PS, Any], *args: Any, **kwargs: Any) -> Any:
        func.retry_num = 0
        func.delay = func_delay_decorator(func, self.queue_name, self.max_retries)
        return func
