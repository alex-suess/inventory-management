"""
Tests for the low-stock alerts API endpoint.
"""
import pytest


class TestLowStockEndpoint:
    """Test suite for /api/inventory/low-stock."""

    def test_get_low_stock_items(self, client):
        """Test that every returned item is at or below its reorder point."""
        response = client.get("/api/inventory/low-stock")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for item in data:
            assert item["quantity_on_hand"] <= item["reorder_point"]

    def test_low_stock_matches_inventory(self, client):
        """Test that the list matches low stock items computed from /api/inventory."""
        all_items = client.get("/api/inventory").json()
        expected = {i["id"] for i in all_items if i["quantity_on_hand"] <= i["reorder_point"]}

        data = client.get("/api/inventory/low-stock").json()
        assert {i["id"] for i in data} == expected

    def test_low_stock_matches_dashboard_summary(self, client):
        """Test that the count matches the dashboard summary."""
        summary = client.get("/api/dashboard/summary").json()
        data = client.get("/api/inventory/low-stock").json()
        assert len(data) == summary["low_stock_items"]

    def test_low_stock_not_shadowed_by_item_id_route(self, client):
        """Test that the path is not captured by /api/inventory/{item_id}."""
        response = client.get("/api/inventory/low-stock")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_low_stock_warehouse_filter(self, client):
        """Test filtering low stock items by warehouse."""
        all_low = client.get("/api/inventory/low-stock").json()
        warehouse = all_low[0]["warehouse"]

        data = client.get(f"/api/inventory/low-stock?warehouse={warehouse}").json()
        assert len(data) > 0
        for item in data:
            assert item["warehouse"] == warehouse

    def test_low_stock_category_filter(self, client):
        """Test filtering low stock items by category."""
        all_low = client.get("/api/inventory/low-stock").json()
        category = all_low[0]["category"]

        data = client.get(f"/api/inventory/low-stock?category={category}").json()
        assert len(data) > 0
        for item in data:
            assert item["category"].lower() == category.lower()

    def test_low_stock_multiple_filters_and_all(self, client):
        """Test combined filters, and that 'all' is ignored."""
        first = client.get("/api/inventory/low-stock").json()[0]
        data = client.get(
            f"/api/inventory/low-stock?warehouse={first['warehouse']}&category={first['category']}"
        ).json()
        for item in data:
            assert item["warehouse"] == first["warehouse"]
            assert item["category"].lower() == first["category"].lower()

        everything = client.get("/api/inventory/low-stock").json()
        with_all = client.get("/api/inventory/low-stock?warehouse=all&category=all").json()
        assert len(with_all) == len(everything)

    def test_low_stock_sorted_most_critical_first(self, client):
        """Test that items are sorted by stock-to-reorder ratio ascending."""
        data = client.get("/api/inventory/low-stock").json()
        ratios = [i["quantity_on_hand"] / i["reorder_point"] for i in data if i["reorder_point"]]
        assert ratios == sorted(ratios)

    def test_low_stock_no_matching_items(self, client):
        """Test that a filter matching nothing returns an empty list."""
        response = client.get("/api/inventory/low-stock?warehouse=Nowhere")
        assert response.status_code == 200
        assert response.json() == []
