from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyKPI",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(unique=True)),
                ("revenue", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("orders", models.PositiveIntegerField(default=0)),
                ("aov", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-date"],
                "verbose_name": "Daily KPI",
                "verbose_name_plural": "Daily KPIs",
            },
        ),
    ]
