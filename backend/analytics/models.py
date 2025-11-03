from __future__ import annotations

from django.db import models


class DailyKPI(models.Model):
    date = models.DateField(unique=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    orders = models.PositiveIntegerField(default=0)
    aov = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Daily KPI"
        verbose_name_plural = "Daily KPIs"

    def __str__(self) -> str:
        return f"{self.date} • revenue={self.revenue} orders={self.orders}"
