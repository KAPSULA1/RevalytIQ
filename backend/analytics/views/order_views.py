from __future__ import annotations
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from core.models import Order


class OrderSerializer(ModelSerializer):
    """🎯 Serializer for recent orders."""
    class Meta:
        model = Order
        fields = ["id", "amount", "status", "created_at"]


class OrderListView(ListAPIView):
    """
    📦 Return the most recent 50 paid orders for analytics.
    Requires authentication.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(status="paid").order_by("-created_at")[:50]
