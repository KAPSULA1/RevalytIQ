from __future__ import annotations
from datetime import datetime, timedelta
from celery import shared_task
from core.services.kpi_service import kpis

@shared_task
def generate_daily_report() -> dict[str, float | int]:
    """Generate KPI report for the previous day."""
    end = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=1)
    return kpis(start, end)
