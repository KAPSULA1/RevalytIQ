from __future__ import annotations
from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.title} ({self.sku})"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[("paid","Paid"),("pending","Pending")], default="paid")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="items")
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.qty * self.unit_price
