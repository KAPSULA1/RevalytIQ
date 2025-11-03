from __future__ import annotations
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """🎯 Serializer for recent orders."""

    customer = serializers.CharField(source="customer.name")

    class Meta:
        model = Order
        fields = ["id", "customer", "amount", "status", "created_at"]


class OrderListView(ListAPIView):
    """
    📦 Return paid orders with pagination for analytics.
    Requires authentication.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(status="paid").order_by("-created_at")
