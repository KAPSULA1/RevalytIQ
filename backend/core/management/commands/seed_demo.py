from __future__ import annotations
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Customer, Product, Order, OrderItem

class Command(BaseCommand):
    help = "Seed demo data for portfolio"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # customers
        customers = []
        for i in range(10):
            c, _ = Customer.objects.get_or_create(
                email=f"customer{i+1}@example.com",
                defaults={"name": f"Customer {i+1}", "created_at": timezone.now()},
            )
            customers.append(c)

        # products
        products = []
        catalog = [
            ("SKU-101", "Starter Plan", Decimal("19.00")),
            ("SKU-201", "Pro Plan", Decimal("49.00")),
            ("SKU-301", "Enterprise Plan", Decimal("99.00")),
            ("SKU-401", "Add-on: Reports", Decimal("9.00")),
            ("SKU-501", "Add-on: Priority Support", Decimal("15.00")),
        ]
        for sku, title, price in catalog:
            p, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={"title": title, "unit_price": price, "created_at": timezone.now()},
            )
            products.append(p)

        # orders (last 60 days)
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        random.seed(42)

        for day_offset in range(60):
            for _ in range(random.randint(0, 4)):
                cust = random.choice(customers)
                created_at = timezone.now() - timezone.timedelta(days=day_offset, hours=random.randint(0,23))
                order = Order.objects.create(customer=cust, status="paid", created_at=created_at)

                items_count = random.randint(1, 3)
                total = Decimal("0.00")
                for _ in range(items_count):
                    prod = random.choice(products)
                    qty = random.randint(1, 5)
                    item = OrderItem.objects.create(
                        order=order,
                        product=prod,
                        qty=qty,
                        unit_price=prod.unit_price,
                    )
                    total += item.unit_price * qty
                order.amount = total
                order.save(update_fields=["amount"])

        self.stdout.write(self.style.SUCCESS("Seed complete!"))
