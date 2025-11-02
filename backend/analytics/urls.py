from django.urls import path
from analytics.views.kpi_views import KPIView
from analytics.views.order_views import OrderListView

urlpatterns = [
    path("kpis/", KPIView.as_view(), name="kpis"),
    path("orders/", OrderListView.as_view(), name="orders"),
]
