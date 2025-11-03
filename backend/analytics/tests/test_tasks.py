from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from analytics.models import DailyKPI
from analytics.tasks import generate_daily_report
from core.models import Customer, Order


class DailyReportTaskTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Report Customer", email="report@example.com")

    def _create_order(self, amount: int, minutes_offset: int = 0) -> None:
        Order.objects.create(
            customer=self.customer,
            amount=amount,
            status="paid",
            created_at=timezone.now() - timedelta(days=1, minutes=minutes_offset),
        )

    def test_generate_daily_report_persists_record(self):
        self._create_order(250, minutes_offset=5)
        self._create_order(150, minutes_offset=15)

        target_date = (timezone.now() - timedelta(days=1)).date()
        result = generate_daily_report.run(target_date.isoformat())

        record = DailyKPI.objects.get(date=target_date)
        self.assertEqual(record.orders, 2)
        self.assertAlmostEqual(float(record.revenue), 400.0)
        self.assertAlmostEqual(float(record.aov), 200.0)
        self.assertEqual(result["orders"], 2)

    def test_generate_daily_report_overwrites_existing(self):
        day = (timezone.now() - timedelta(days=1)).date()
        DailyKPI.objects.create(date=day, revenue=0, orders=0, aov=0)

        self._create_order(100)
        generate_daily_report.run(day.isoformat())

        record = DailyKPI.objects.get(date=day)
        self.assertEqual(record.orders, 1)
