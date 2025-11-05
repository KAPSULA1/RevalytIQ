from __future__ import annotations

import random
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import Customer, Order, OrderItem, Product


class Command(BaseCommand):
    help = "Populate demo data and user for the Render free-tier deployment."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fail-safe",
            action="store_true",
            help="Do not raise if the seed already exists; exit quietly instead.",
        )

    def handle(self, *args, **options):
        if not getattr(settings, "ENABLE_DEMO_SEED", True):
            self.stdout.write("ENABLE_DEMO_SEED is disabled; skipping.")
            return

        User = get_user_model()

        if User.objects.filter(username="demo").exists():
            if options["fail_safe"]:
                self.stdout.write("Demo user already exists; skipping seed.")
                return
            raise SystemExit("Demo seed already present. Use --fail-safe to ignore.")

        with transaction.atomic():
            user = User.objects.create_user(
                username="demo",
                email="demo@revalytiq.com",
                password="password123",
                first_name="Demo",
                last_name="User",
            )
            self.stdout.write(f"Created demo user {user.username} / password123")

            customers = []
            for i in range(10):
                customer, _ = Customer.objects.get_or_create(
                    email=f"customer{i+1}@example.com",
                    defaults={
                        "name": f"Customer {i+1}",
                        "created_at": timezone.now() - timezone.timedelta(days=i),
                    },
                )
                customers.append(customer)

            catalog = [
                ("SKU-101", "Starter Plan", Decimal("19.00")),
                ("SKU-201", "Pro Plan", Decimal("49.00")),
                ("SKU-301", "Enterprise Plan", Decimal("99.00")),
                ("SKU-401", "Add-on: Reports", Decimal("9.00")),
                ("SKU-501", "Add-on: Priority Support", Decimal("15.00")),
            ]
            products = []
            for sku, title, price in catalog:
                product, _ = Product.objects.get_or_create(
                    sku=sku,
                    defaults={
                        "title": title,
                        "unit_price": price,
                        "created_at": timezone.now(),
                    },
                )
                products.append(product)

            OrderItem.objects.all().delete()
            Order.objects.all().delete()

            random.seed(42)
            now = timezone.now()
            for day_offset in range(60):
                order_count = random.randint(1, 4)
                for _ in range(order_count):
                    customer = random.choice(customers)
                    created_at = now - timezone.timedelta(
                        days=day_offset, hours=random.randint(0, 23)
                    )
                    order = Order.objects.create(
                        customer=customer,
                        status="paid",
                        created_at=created_at,
                    )
                    total = Decimal("0.00")
                    for _ in range(random.randint(1, 3)):
                        product = random.choice(products)
                        qty = random.randint(1, 5)
                        line_total = product.unit_price * qty
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            qty=qty,
                            unit_price=product.unit_price,
                        )
                        total += line_total
                    order.amount = total
                    order.save(update_fields=["amount"])

        self.stdout.write(self.style.SUCCESS("Demo dataset loaded."))
