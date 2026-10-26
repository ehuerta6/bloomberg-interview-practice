import asyncio
from contextlib import closing

import httpx
import pytest
from fastapi.testclient import TestClient

from app.db import connect, reset, seed
from app.main import app


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "checkout.sqlite3"
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


def add_to_cart(client, product_id=BERRY, quantity=1, headers=SHOPPER):
    return client.post(
        "/cart/items",
        headers=headers,
        json={"product_id": product_id, "quantity": quantity},
    )


def checkout(client, key, outcome="success", headers=SHOPPER):
    return client.post(
        "/checkout",
        headers={**headers, "Idempotency-Key": key},
        json={"payment_outcome": outcome},
    )


def test_successful_checkout_persists_order_snapshots_stock_and_clears_cart(client):
    add_to_cart(client, BERRY, 2)
    add_to_cart(client, DUCK, 1)

    response = checkout(client, "order-river-1")

    assert response.status_code == 201
    order = response.json()
    assert order["status"] == "placed"
    assert order["total_cents"] == 1749
    assert order["items"] == [
        {
            "product_id": BERRY,
            "name": "Berry Bowl",
            "category": "food",
            "price_cents": 425,
            "quantity": 2,
            "line_total_cents": 850,
        },
        {
            "product_id": DUCK,
            "name": "Floating Duck",
            "category": "toys",
            "price_cents": 899,
            "quantity": 1,
            "line_total_cents": 899,
        },
    ]
    stock = {product["id"]: product["stock"] for product in client.get("/products").json()}
    assert stock[BERRY] == 10
    assert stock[DUCK] == 4
    assert client.get("/cart", headers=SHOPPER).json() == {"items": [], "total_cents": 0}


def test_line_persistence_failure_leaves_checkout_state_unchanged(client, database):
    add_to_cart(client, BERRY, 2)
    with closing(connect(database)) as connection:
        connection.execute(
            """CREATE TRIGGER reject_berry_order_line BEFORE INSERT ON order_items
               WHEN NEW.product_id = 'food-berry-bowl'
               BEGIN SELECT RAISE(ABORT, 'controlled order-line failure'); END"""
        )
        connection.commit()

    response = checkout(client, "controlled-line-failure")

    with closing(connect(database)) as connection:
        orders = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        order_lines = connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
        stock = connection.execute(
            "SELECT stock FROM products WHERE id = ?", (BERRY,)
        ).fetchone()[0]

    assert (
        response.status_code,
        orders,
        order_lines,
        stock,
        client.get("/cart", headers=SHOPPER).json()["items"][0]["quantity"],
    ) == (503, 0, 0, 12, 2)


def test_reset_restarts_order_ids_from_the_initial_state(client, database):
    add_to_cart(client, BERRY)
    first = checkout(client, "order-before-reset")
    assert first.status_code == 201
    assert first.json()["id"] == 1

    with closing(connect(database)) as connection:
        reset(connection)

    add_to_cart(client, BERRY)
    after_reset = checkout(client, "order-after-reset")

    assert after_reset.status_code == 201
    assert after_reset.json()["id"] == first.json()["id"]


def test_repeated_success_with_same_key_returns_the_existing_order(client, database):
    add_to_cart(client, BERRY, 2)

    first = checkout(client, "order-river-2")
    replay = checkout(client, "order-river-2")
    different_request = checkout(client, "order-river-2", "decline")

    assert first.status_code == 201
    assert replay.status_code == 200
    assert replay.json() == first.json()
    assert different_request.status_code == 409
    assert client.get("/products/food-berry-bowl").json()["stock"] == 10
    with closing(connect(database)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1


@pytest.mark.parametrize(
    ("outcome", "expected_status", "detail"),
    [
        ("decline", 402, "Payment declined"),
        ("temporary_error", 503, "Temporary payment error"),
    ],
)
def test_failed_payment_replays_without_order_or_stock_change(
    client, database, outcome, expected_status, detail
):
    add_to_cart(client, BERRY, 2)

    first = checkout(client, f"failed-{outcome}", outcome)
    replay = checkout(client, f"failed-{outcome}", outcome)
    different_request = checkout(client, f"failed-{outcome}", "success")

    assert first.status_code == replay.status_code == expected_status
    assert first.json() == replay.json() == {"detail": detail}
    assert different_request.status_code == 409
    assert client.get("/products/food-berry-bowl").json()["stock"] == 12
    assert client.get("/cart", headers=SHOPPER).json()["items"][0]["quantity"] == 2
    with closing(connect(database)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM checkout_attempts").fetchone()[0] == 1


def test_insufficient_stock_is_atomic_and_idempotent(client, database):
    add_to_cart(client, BERRY, 3)
    client.put(
        f"/admin/products/{BERRY}",
        headers=ADMIN,
        json={"name": "Berry Bowl", "category": "food", "price_cents": 425, "stock": 2},
    )

    first = checkout(client, "order-short-stock")
    client.put(
        f"/admin/products/{BERRY}",
        headers=ADMIN,
        json={"name": "Berry Bowl", "category": "food", "price_cents": 425, "stock": 3},
    )
    replay = checkout(client, "order-short-stock")

    assert first.status_code == replay.status_code == 409
    assert first.json() == replay.json() == {"detail": "Insufficient stock"}
    assert client.get("/products/food-berry-bowl").json()["stock"] == 3
    assert client.get("/cart", headers=SHOPPER).json()["items"][0]["quantity"] == 3
    with closing(connect(database)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0


def test_order_replay_preserves_purchased_product_details(client):
    add_to_cart(client, BERRY, 2)
    first = checkout(client, "snapshot-order")
    client.put(
        f"/admin/products/{BERRY}",
        headers=ADMIN,
        json={"name": "New Berry Bowl", "category": "food", "price_cents": 700, "stock": 10},
    )

    replay = checkout(client, "snapshot-order")

    assert replay.status_code == 200
    assert replay.json() == first.json()
    assert replay.json()["items"][0]["name"] == "Berry Bowl"
    assert replay.json()["items"][0]["price_cents"] == 425


def test_same_idempotency_key_is_scoped_to_each_shopper(client, database):
    with closing(connect(database)) as connection:
        connection.execute(
            "INSERT INTO users (id, name, role) VALUES (?, ?, ?)",
            ("shopper-lagoon", "Lani Lagoon", "shopper"),
        )
        connection.execute("INSERT INTO carts (user_id) VALUES (?)", ("shopper-lagoon",))
        connection.commit()
    second_shopper = {"X-User-Id": "shopper-lagoon"}
    add_to_cart(client, BERRY, 1, SHOPPER)
    add_to_cart(client, BERRY, 1, second_shopper)

    first_order = checkout(client, "shared-local-key", headers=SHOPPER)
    second_order = checkout(client, "shared-local-key", headers=second_shopper)

    assert first_order.status_code == second_order.status_code == 201
    assert first_order.json()["id"] != second_order.json()["id"]
    assert client.get("/products/food-berry-bowl").json()["stock"] == 10


def test_checkout_requires_a_valid_shopper_key_and_outcome(client):
    assert client.post("/checkout", headers=SHOPPER, json={}).status_code == 422
    assert client.post(
        "/checkout", headers={**SHOPPER, "Idempotency-Key": " "}, json={}
    ).status_code == 422
    assert checkout(client, "unknown-outcome", "maybe").status_code == 422
    assert client.post(
        "/checkout",
        headers={"X-User-Id": "missing-user", "Idempotency-Key": "unknown"},
        json={},
    ).status_code == 401
    assert client.post(
        "/checkout", headers={**ADMIN, "Idempotency-Key": "admin"}, json={}
    ).status_code == 403


def test_empty_cart_result_is_replayed_for_the_same_key(client, database):
    first = checkout(client, "empty-cart")
    replay = checkout(client, "empty-cart")

    assert first.status_code == replay.status_code == 409
    assert first.json() == replay.json() == {"detail": "Cart is empty"}
    with closing(connect(database)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM checkout_attempts").fetchone()[0] == 1


def test_concurrent_checkouts_with_same_key_create_only_one_order(client, database):
    add_to_cart(client, BERRY, 2)

    async def submit_both():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as session:
            headers = {**SHOPPER, "Idempotency-Key": "concurrent-order"}
            request = {"payment_outcome": "success"}
            return await asyncio.gather(
                session.post("/checkout", headers=headers, json=request),
                session.post("/checkout", headers=headers, json=request),
            )

    first, second = asyncio.run(submit_both())

    assert sorted([first.status_code, second.status_code]) == [200, 201]
    assert first.json()["id"] == second.json()["id"]
    assert client.get("/products/food-berry-bowl").json()["stock"] == 10
    with closing(connect(database)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1


def test_reset_clears_orders_attempts_stock_changes_and_cart_state(client, database):
    add_to_cart(client, BERRY, 2)
    checkout(client, "reset-checkout")

    with closing(connect(database)) as connection:
        reset(connection)
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM checkout_attempts").fetchone()[0] == 0

    assert client.get("/products/food-berry-bowl").json()["stock"] == 12
    assert client.get("/cart", headers=SHOPPER).json() == {"items": [], "total_cents": 0}
