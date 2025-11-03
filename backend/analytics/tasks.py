from __future__ import annotations
from datetime import datetime, time, timedelta
from decimal import Decimal

from celery import shared_task
from django.utils import timezone

from analytics.models import DailyKPI
from core.services.kpi_service import kpis


def _normalize_decimal(value: float | int) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=3600,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def generate_daily_report(self, target_date: str | None = None) -> dict[str, float | int]:
    """Persist KPI aggregates for the requested day (defaults to yesterday UTC)."""

    if target_date:
        try:
            day = datetime.fromisoformat(target_date).date()
        except ValueError as exc:  # pragma: no cover - guardrail
            raise ValueError("target_date must be ISO formatted YYYY-MM-DD") from exc
    else:
        day = (timezone.now() - timedelta(days=1)).date()

    start_dt = timezone.make_aware(datetime.combine(day, time.min))
    end_dt = start_dt + timedelta(days=1)

    aggregates = kpis(start_dt, end_dt)

    report, _created = DailyKPI.objects.update_or_create(
        date=day,
        defaults={
            "revenue": _normalize_decimal(aggregates["revenue"]),
            "orders": int(aggregates["orders"]),
            "aov": _normalize_decimal(aggregates["aov"]),
        },
    )

    return {
        "date": str(report.date),
        "revenue": float(report.revenue),
        "orders": report.orders,
        "aov": float(report.aov),
    }
