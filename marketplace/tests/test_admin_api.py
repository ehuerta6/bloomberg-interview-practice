from contextlib import closing

import pytest
from fastapi.testclient import TestClient

from app.db import connect, seed
from app.main import app


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "admin.sqlite3"
    monkeypatch.setenv("CAPPY_DB_PATH", str(path))
    with closing(connect(path)) as connection:
        seed(connection)
    return path


@pytest.fixture
def client(database):
    with TestClient(app) as test_client:
        yield test_client


ADMIN = {"X-User-Id": "admin-stone"}
SHOPPER = {"X-User-Id": "shopper-river"}
PRODUCT = "food-berry-bowl"


@pytest.mark.parametrize("delta", [3, -4])
def test_admin_adjusts_stock_atomically(client, delta):
    response = client.post(
        f"/admin/products/{PRODUCT}/stock-adjustments",
        headers=ADMIN,
        json={"delta": delta},
    )

    assert response.status_code == 200
    assert response.json() == {"product_id": PRODUCT, "delta": delta, "stock": 12 + delta}
    with closing(connect()) as connection:
        assert connection.execute(
            "SELECT stock FROM products WHERE id = ?", (PRODUCT,)
        ).fetchone()[0] == 12 + delta


@pytest.mark.parametrize(
    "payload", [{"delta": 0}, {"delta": 2**63}, {"delta": True}, {"delta": 1.5}, {"delta": 1, "other": 2}]
)
def test_invalid_stock_adjustments_are_rejected_without_changes(client, payload):
    response = client.post(
        f"/admin/products/{PRODUCT}/stock-adjustments", headers=ADMIN, json=payload
    )

    assert response.status_code == 422
    with closing(connect()) as connection:
        assert connection.execute(
            "SELECT stock FROM products WHERE id = ?", (PRODUCT,)
        ).fetchone()[0] == 12


def test_stock_adjustment_cannot_underflow(client):
    response = client.post(
        f"/admin/products/{PRODUCT}/stock-adjustments",
        headers=ADMIN,
        json={"delta": -13},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Stock adjustment would exceed valid stock"}
    with closing(connect()) as connection:
        assert connection.execute(
            "SELECT stock FROM products WHERE id = ?", (PRODUCT,)
        ).fetchone()[0] == 12


def test_stock_adjustment_cannot_overflow_sqlite_integer(client, database):
    with closing(connect(database)) as connection, connection:
        connection.execute(
            "UPDATE products SET stock = ? WHERE id = ?", (2**63 - 1, PRODUCT)
        )

    response = client.post(
        f"/admin/products/{PRODUCT}/stock-adjustments",
        headers=ADMIN,
        json={"delta": 1},
    )

    assert response.status_code == 409
    with closing(connect(database)) as connection:
        assert connection.execute(
            "SELECT stock FROM products WHERE id = ?", (PRODUCT,)
        ).fetchone()[0] == 2**63 - 1


def test_stock_adjustment_reports_unknown_product(client):
    response = client.post(
        "/admin/products/missing/stock-adjustments", headers=ADMIN, json={"delta": 1}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


@pytest.mark.parametrize(
    ("headers", "expected"),
    [(SHOPPER, 403), ({"X-User-Id": "unknown"}, 401), ({}, 401)],
)
def test_non_admin_cannot_use_admin_operations(client, headers, expected):
    assert client.get("/admin/orders", headers=headers).status_code == expected
    assert (
        client.post(
            f"/admin/products/{PRODUCT}/stock-adjustments",
            headers=headers,
            json={"delta": 1},
        ).status_code
        == expected
    )
    assert client.get("/admin/orders", headers=ADMIN).json() == []


def test_admin_reads_all_orders_in_stable_order_with_snapshots(client, database):
    with closing(connect(database)) as connection, connection:
        for user_id, product_name, price, quantity in [
            ("shopper-river", "Historical Berry", 400, 2),
            ("shopper-river", "Old Stone", 250, 1),
        ]:
            cursor = connection.execute(
                "INSERT INTO orders (user_id, status, total_cents) VALUES (?, 'placed', ?)",
                (user_id, price * quantity),
            )
            connection.execute(
                """INSERT INTO order_items
                   (order_id, product_id, product_name, category, price_cents,
                    quantity, line_total_cents)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (cursor.lastrowid, PRODUCT, product_name, "food", price, quantity, price * quantity),
            )

    first = client.get("/admin/orders", headers=ADMIN)
    second = client.get("/admin/orders", headers=ADMIN)

    assert first.status_code == 200
    assert first.json() == second.json()
    orders = first.json()
    assert [order["id"] for order in orders] == sorted(order["id"] for order in orders)
    assert orders[0]["items"] == [
        {
            "product_id": PRODUCT,
            "name": "Historical Berry",
            "category": "food",
            "price_cents": 400,
            "quantity": 2,
            "line_total_cents": 800,
        }
    ]


def test_admin_order_views_do_not_change_order_state(client, database):
    with closing(connect(database)) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO orders (user_id, status, total_cents) VALUES (?, 'placed', ?)",
            ("shopper-river", 800),
        )
        order_id = cursor.lastrowid
        connection.execute(
            """INSERT INTO order_items
               (order_id, product_id, product_name, category, price_cents,
                quantity, line_total_cents)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (order_id, PRODUCT, "Berry Bowl", "food", 400, 2, 800),
        )

    unsupported = client.post(f"/admin/orders/{order_id}/cancel", headers=ADMIN)
    listing = client.get("/admin/orders", headers=ADMIN).json()

    assert unsupported.status_code == 404
    assert listing[0]["status"] == "placed"
    assert client.get(f"/products/{PRODUCT}").json()["stock"] == 12


def test_admin_can_read_one_order(client, database):
    with closing(connect(database)) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO orders (user_id, status, total_cents) VALUES (?, 'placed', 800)",
            ("shopper-river",),
        )
        order_id = cursor.lastrowid

    response = client.get(f"/admin/orders/{order_id}", headers=ADMIN)

    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["user_id"] == "shopper-river"
    assert response.json()["total_cents"] == 800
