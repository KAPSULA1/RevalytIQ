from __future__ import annotations
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.services.kpi_service import kpis
from core.utils.date_ranges import parse_range


class KPIView(APIView):
    """
    📊 Return computed KPI metrics for the analytics dashboard.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start, end = parse_range(
            request.query_params.get("start"),
            request.query_params.get("end"),
        )

        data = kpis(start, end)
        return Response(data)
