from __future__ import annotations
from rest_framework import serializers
from core.models import Order

class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "amount_cents", "amount", "status", "created_at"]
        read_only_fields = ["id", "amount", "created_at"]
