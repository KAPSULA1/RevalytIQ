from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Customer, Product, Order, OrderItem
from django.utils import timezone

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
        """✅ Orders endpoint should return a list of orders"""
        response = self.client.get("/api/analytics/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        if response.data:
            order = response.data[0]
            self.assertIn("id", order)
            self.assertIn("amount", order)
            self.assertIn("status", order)
