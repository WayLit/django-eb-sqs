from __future__ import annotations

from typing import Any


class RetryableTaskException(Exception):  # noqa: N818
    def __init__(
        self,
        inner: Exception,
        delay: int | None = None,
        count_retries: bool | None = None,
        max_retries_func: Any = None,
    ) -> None:
        self._inner = inner

        self.delay = delay
        self.count_retries = count_retries
        self.max_retries_func = max_retries_func

    def __repr__(self) -> str:
        return repr(self._inner)
