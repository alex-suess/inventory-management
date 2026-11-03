"""
Tests for reports API endpoints.
"""
import pytest


class TestReportsEndpoints:
    """Test suite for report endpoints and the global filters they accept."""

    def test_get_quarterly_reports(self, client):
        """Test getting quarterly reports without filters."""
        response = client.get("/api/reports/quarterly")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for key in ["quarter", "total_orders", "total_revenue", "avg_order_value", "fulfillment_rate"]:
            assert key in data[0]

    def test_get_monthly_trends(self, client):
        """Test getting monthly trends without filters."""
        response = client.get("/api/reports/monthly-trends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for key in ["month", "order_count", "revenue", "delivered_count"]:
            assert key in data[0]

    def test_monthly_trends_warehouse_filter_matches_orders(self, client):
        """Filtered trends must account for exactly the orders /api/orders returns."""
        orders = client.get("/api/orders?warehouse=Tokyo").json()
        trends = client.get("/api/reports/monthly-trends?warehouse=Tokyo").json()

        assert sum(m["order_count"] for m in trends) == len(orders)
        assert sum(m["order_count"] for m in trends) < sum(
            m["order_count"] for m in client.get("/api/reports/monthly-trends").json()
        )

    def test_quarterly_reports_status_filter(self, client):
        """Test that the status filter narrows the quarterly totals."""
        all_total = sum(q["total_orders"] for q in client.get("/api/reports/quarterly").json())
        delivered = client.get("/api/reports/quarterly?status=Delivered").json()

        assert sum(q["total_orders"] for q in delivered) < all_total
        for q in delivered:
            assert q["fulfillment_rate"] == 100.0

    def test_monthly_trends_month_filter(self, client):
        """Test that a single-month filter returns only that month."""
        data = client.get("/api/reports/monthly-trends?month=2025-01").json()

        assert len(data) <= 1
        for m in data:
            assert m["month"] == "2025-01"

    def test_reports_no_matching_orders(self, client):
        """Test that filters matching nothing return empty lists, not errors."""
        for path in ["quarterly", "monthly-trends"]:
            response = client.get(f"/api/reports/{path}?warehouse=Nowhere")
            assert response.status_code == 200
            assert response.json() == []
