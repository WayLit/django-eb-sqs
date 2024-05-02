from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from django.db import close_old_connections, reset_queries


@contextmanager
def django_db_management() -> Generator[None, None, None]:
    reset_queries()
    close_old_connections()
    try:
        yield
    finally:
        close_old_connections()
