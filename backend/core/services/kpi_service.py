from __future__ import annotations
from datetime import datetime
from django.db.models import Sum, Count
from core.models import Order


def kpis(start: datetime, end: datetime) -> dict[str, float | int]:
    """
    Compute key business KPIs (Key Performance Indicators)
    for all paid orders within the given date range.
    """
    qs = Order.objects.filter(
        created_at__gte=start,
        created_at__lt=end,
        status="paid",
    )

    totals = qs.aggregate(
        revenue=Sum("amount"),
        orders=Count("id"),
    )

    revenue = float(totals.get("revenue") or 0)
    orders = int(totals.get("orders") or 0)
    aov = round(revenue / orders, 2) if orders else 0.0

    return {
        "revenue": revenue,
        "orders": orders,
        "aov": aov,
    }
