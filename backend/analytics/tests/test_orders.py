from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Customer, Product, Order, OrderItem

User = get_user_model()


class OrdersTests(APITestCase):
    """🔍 Integration test for the Orders analytics endpoint"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="pass1234"
        )
        self.client.force_authenticate(user=self.user)

        customer = Customer.objects.create(name="Alice", email="alice@example.com")
        product = Product.objects.create(sku="SKU001", title="Test Product", unit_price=50)

        order = Order.objects.create(
            customer=customer,
            amount=100,
            status="paid",
            created_at=timezone.now()
        )

        OrderItem.objects.create(order=order, product=product, qty=2, unit_price=50)

    def test_orders_list(self):
        """✅ Orders endpoint should return a paginated response"""
        response = self.client.get("/api/analytics/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data
        self.assertIn("results", payload)
        self.assertIn("count", payload)
        self.assertEqual(payload["count"], 1)
        first = payload["results"][0]
        self.assertIn("customer", first)
        self.assertEqual(first["customer"], "Alice")

    def test_orders_pagination_second_page(self):
        """📄 Pagination should work when requesting subsequent pages"""
        customer = Customer.objects.first()
        for i in range(60):
            Order.objects.create(
                customer=customer,
                amount=10,
                status="paid",
                created_at=timezone.now() + timedelta(minutes=i + 1),
            )

        response = self.client.get("/api/analytics/orders/?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data
        self.assertIn("results", payload)
        self.assertGreater(payload["count"], 50)
        self.assertTrue(len(payload["results"]) > 0)
