from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, BrokenBarrierError

from fastapi.testclient import TestClient
import pytest

from app.db import connect, seed
from app.main import app
from app import orders


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "orders.sqlite3"
    monkeypatch.setenv("CAPPY_DB_PATH", str(path))
    with closing(connect(path)) as connection:
        seed(connection)
    return path


@pytest.fixture
def client(database):
    with TestClient(app) as test_client:
        yield test_client


SHOPPER = {"X-User-Id": "shopper-river"}
ADMIN = {"X-User-Id": "admin-stone"}
BERRY = "food-berry-bowl"
DUCK = "toy-floating-duck"


def place_order(client, key="orders-test", headers=SHOPPER):
    for product_id, quantity in [(BERRY, 2), (DUCK, 1)]:
        response = client.post(
            "/cart/items",
            headers=headers,
            json={"product_id": product_id, "quantity": quantity},
        )
        assert response.status_code == 200
    return client.post(
        "/checkout",
        headers={**headers, "Idempotency-Key": key},
        json={"payment_outcome": "success"},
    )


def test_shopper_lists_and_retrieves_owned_order_with_line_snapshots(client):
    placed = place_order(client)

    listing = client.get("/orders", headers=SHOPPER)
    detail = client.get(f"/orders/{placed.json()['id']}", headers=SHOPPER)

    assert listing.status_code == detail.status_code == 200
    assert listing.json() == [placed.json()]
    assert detail.json() == placed.json()
    assert detail.json()["items"][0]["name"] == "Berry Bowl"
    assert detail.json()["items"][0]["quantity"] == 2


def test_cancel_restores_stock_and_persists_cancelled_status(client):
    placed = place_order(client)
    order_id = placed.json()["id"]
    assert client.get(f"/products/{BERRY}").json()["stock"] == 10
    assert client.get(f"/products/{DUCK}").json()["stock"] == 4

    cancelled = client.post(f"/orders/{order_id}/cancel", headers=SHOPPER)

    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert cancelled.json()["items"] == placed.json()["items"]
    assert client.get(f"/products/{BERRY}").json()["stock"] == 12
    assert client.get(f"/products/{DUCK}").json()["stock"] == 5
    assert client.get(f"/orders/{order_id}", headers=SHOPPER).json()["status"] == "cancelled"


def test_repeated_cancel_returns_conflict_without_restoring_stock_twice(client):
    order_id = place_order(client).json()["id"]
    first = client.post(f"/orders/{order_id}/cancel", headers=SHOPPER)
    repeated = client.post(f"/orders/{order_id}/cancel", headers=SHOPPER)

    assert first.status_code == 200
    assert repeated.status_code == 409
    assert client.get(f"/products/{BERRY}").json()["stock"] == 12
    assert client.get(f"/products/{DUCK}").json()["stock"] == 5


def test_overlapping_cancellations_restore_inventory_once(client, database, monkeypatch):
    order_id = place_order(client).json()["id"]
    original_read = orders.read_order_status
    both_have_read = Barrier(2, timeout=3)

    def synchronized_read(connection, requested_order_id, user_id):
        result = original_read(connection, requested_order_id, user_id)
        try:
            both_have_read.wait()
        except BrokenBarrierError:
            pass
        return result

    monkeypatch.setattr(orders, "read_order_status", synchronized_read)

    def cancel_once():
        with TestClient(app) as concurrent_client:
            return concurrent_client.post(f"/orders/{order_id}/cancel", headers=SHOPPER)

    with ThreadPoolExecutor(max_workers=2) as executor:
        responses = list(executor.map(lambda _: cancel_once(), range(2)))
    with closing(connect(database)) as connection:
        persisted_status = connection.execute(
            "SELECT status FROM orders WHERE id = ?", (order_id,)
        ).fetchone()["status"]
        stock = {
            product_id: connection.execute(
                "SELECT stock FROM products WHERE id = ?", (product_id,)
            ).fetchone()[0]
            for product_id in (BERRY, DUCK)
        }

    assert (
        sorted(response.status_code for response in responses),
        persisted_status,
        stock,
    ) == ([200, 409], "cancelled", {BERRY: 12, DUCK: 5})


def test_other_shoppers_cannot_list_or_access_order(client, database):
    placed = place_order(client)
    with closing(connect(database)) as connection:
        connection.execute(
            "INSERT INTO users (id, name, role) VALUES (?, ?, ?)",
            ("shopper-lagoon", "Lani Lagoon", "shopper"),
        )
        connection.commit()

    other = {"X-User-Id": "shopper-lagoon"}
    assert client.get("/orders", headers=other).json() == []
    assert client.get(f"/orders/{placed.json()['id']}", headers=other).status_code == 404
    assert client.post(f"/orders/{placed.json()['id']}/cancel", headers=other).status_code == 404
    assert client.get(f"/products/{BERRY}").json()["stock"] == 10


def test_unknown_order_is_404_and_invalid_status_cancel_is_409(client):
    assert client.get("/orders/999", headers=SHOPPER).status_code == 404
    assert client.post("/orders/999/cancel", headers=SHOPPER).status_code == 404
    order_id = place_order(client).json()["id"]
    assert client.post(f"/orders/{order_id}/cancel", headers=ADMIN).status_code == 403
    assert client.post(f"/orders/{order_id}/cancel", headers={}).status_code == 401

    cancelled = client.post(f"/orders/{order_id}/cancel", headers=SHOPPER)
    invalid_repeat = client.post(f"/orders/{order_id}/cancel", headers=SHOPPER)
    assert cancelled.status_code == 200
    assert invalid_repeat.status_code == 409


def test_stock_restore_failure_rolls_back_status_and_prior_line_updates(client, database):
    placed = place_order(client)
    with closing(connect(database)) as connection:
        connection.execute("DELETE FROM products WHERE id = ?", (DUCK,))
        connection.commit()

    failed = client.post(f"/orders/{placed.json()['id']}/cancel", headers=SHOPPER)

    assert failed.status_code == 409
    assert failed.json() == {"detail": "Order inventory could not be restored"}
    with closing(connect(database)) as connection:
        order = connection.execute(
            "SELECT status FROM orders WHERE id = ?", (placed.json()["id"],)
        ).fetchone()
        assert order["status"] == "placed"
        berry_stock = connection.execute(
            "SELECT stock FROM products WHERE id = ?", (BERRY,)
        ).fetchone()[0]
        assert berry_stock == 10


def test_stock_ceiling_failure_rolls_back_status_and_prior_line_updates(client, database):
    placed = place_order(client)
    with closing(connect(database)) as connection:
        connection.execute(
            "UPDATE products SET stock = ? WHERE id = ?", (2**63 - 1, DUCK)
        )
        connection.commit()

    failed = client.post(f"/orders/{placed.json()['id']}/cancel", headers=SHOPPER)

    assert failed.status_code == 409
    assert failed.json() == {"detail": "Order inventory could not be restored"}
    with closing(connect(database)) as connection:
        order = connection.execute(
            "SELECT status FROM orders WHERE id = ?", (placed.json()["id"],)
        ).fetchone()
        assert order["status"] == "placed"
        berry_stock = connection.execute(
            "SELECT stock FROM products WHERE id = ?", (BERRY,)
        ).fetchone()[0]
        duck_stock = connection.execute(
            "SELECT stock FROM products WHERE id = ?", (DUCK,)
        ).fetchone()[0]
        assert berry_stock == 10
        assert duck_stock == 2**63 - 1
