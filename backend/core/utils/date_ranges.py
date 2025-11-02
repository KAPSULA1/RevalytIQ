from __future__ import annotations
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def parse_range(start_iso: str | None, end_iso: str | None) -> tuple[datetime, datetime]:
    """
    Parse ISO datetime strings (UTC) and return timezone-aware datetime objects.
    Defaults to the last 30 days if parameters are missing.
    """
    now = timezone.now()

    try:
        start = timezone.make_aware(datetime.fromisoformat(start_iso)) if start_iso else now - relativedelta(days=30)
    except Exception:
        start = now - relativedelta(days=30)

    try:
        end = timezone.make_aware(datetime.fromisoformat(end_iso)) if end_iso else now
    except Exception:
        end = now

    return start, end
