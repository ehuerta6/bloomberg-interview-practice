from contextlib import closing

from fastapi.testclient import TestClient
import pytest

from app.db import connect, seed
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "smoke.sqlite3"
    monkeypatch.setenv("CAPPY_DB_PATH", str(database))
    with closing(connect(database)) as connection:
        seed(connection)
    with TestClient(app) as test_client:
        yield test_client


def test_seeded_marketplace_smoke_workflow(client):
    shopper = {"X-User-Id": "shopper-river"}
    admin = {"X-User-Id": "admin-stone"}
    product_id = "food-berry-bowl"

    catalog = client.get("/products")
    assert catalog.status_code == 200
    assert catalog.json()[0] == {
        "id": product_id,
        "name": "Berry Bowl",
        "category": "food",
        "price_cents": 425,
        "stock": 12,
    }

    added = client.post(
        "/cart/items", headers=shopper, json={"product_id": product_id, "quantity": 2}
    )
    assert added.status_code == 200
    assert added.json()["total_cents"] == 850

    checkout = client.post(
        "/checkout",
        headers={**shopper, "Idempotency-Key": "onboarding-smoke-order"},
        json={"payment_outcome": "success"},
    )
    assert checkout.status_code == 201
    order = checkout.json()
    assert order["total_cents"] == 850
    assert order["items"][0]["name"] == "Berry Bowl"
    assert client.get("/cart", headers=shopper).json() == {"items": [], "total_cents": 0}
    assert client.get(f"/orders/{order['id']}", headers=shopper).json() == order
    assert client.get("/products/food-berry-bowl").json()["stock"] == 10

    admin_orders = client.get("/admin/orders", headers=admin)
    assert admin_orders.status_code == 200
    assert [item["id"] for item in admin_orders.json()] == [order["id"]]

    adjustment = client.post(
        f"/admin/products/{product_id}/stock-adjustments",
        headers=admin,
        json={"delta": 3},
    )
    assert adjustment.status_code == 200
    assert adjustment.json()["stock"] == 13
    assert client.get("/products/food-berry-bowl").json()["stock"] == 13

    forbidden = client.post(
        f"/admin/products/{product_id}/stock-adjustments",
        headers=shopper,
        json={"delta": 1},
    )
    assert forbidden.status_code == 403
    assert client.get("/products/food-berry-bowl").json()["stock"] == 13
