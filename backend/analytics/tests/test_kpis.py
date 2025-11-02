from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Customer, Order
from django.utils import timezone

User = get_user_model()


class KPITests(APITestCase):
    """🔍 Integration test for the KPI analytics endpoint"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="pass1234"
        )
        self.client.force_authenticate(user=self.user)

        customer = Customer.objects.create(
            name="John Doe", email="john@example.com"
        )

        # ორ-ნახევარი მაგალითი
        Order.objects.create(customer=customer, amount=200, status="paid", created_at=timezone.now())
        Order.objects.create(customer=customer, amount=300, status="paid", created_at=timezone.now())
        Order.objects.create(customer=customer, amount=100, status="pending", created_at=timezone.now())

    def test_kpi_endpoint(self):
        """✅ KPI endpoint returns correct structure and values"""
        response = self.client.get("/api/analytics/kpis/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertIn("revenue", data)
        self.assertIn("orders", data)
        self.assertIn("aov", data)

        # 2 paid orders (200 + 300 = 500 total)
        self.assertEqual(round(data["revenue"], 2), 500.00)
        self.assertEqual(data["orders"], 2)
        self.assertEqual(data["aov"], 250.00)
