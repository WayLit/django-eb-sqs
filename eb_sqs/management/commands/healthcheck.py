from __future__ import annotations

import logging
import sys
from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from eb_sqs import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Checks the SQS worker is healthy, and if not returns a failure code"

    def handle(self, *args, **options) -> None:
        try:
            with open(settings.HEALTHCHECK_FILE_NAME) as file:
                last_healthcheck_date = parse_datetime(file.readlines()[0])

                if (
                    not last_healthcheck_date
                ) or last_healthcheck_date < timezone.now() - timedelta(
                    seconds=settings.HEALTHCHECK_UNHEALTHY_PERIOD_S
                ):
                    self._return_failure()
        except Exception:  # noqa: BLE001
            self._return_failure()

    @staticmethod
    def _return_failure() -> None:
        logger.warning("[django-eb-sqs] Health check failed")
        sys.exit(1)
