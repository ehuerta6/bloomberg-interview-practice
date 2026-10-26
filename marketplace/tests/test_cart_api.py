from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, BrokenBarrierError

import pytest
from fastapi.testclient import TestClient

from app.db import connect, seed
from app.main import app
from app import cart


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "cart.sqlite3"
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
PRODUCT = "food-berry-bowl"


def test_shopper_can_add_change_and_remove_cart_quantities(client):
    added = client.post(
        "/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 2}
    )
    assert added.status_code == 200
    assert added.json() == {
        "items": [
            {
                "product_id": PRODUCT,
                "name": "Berry Bowl",
                "category": "food",
                "price_cents": 425,
                "quantity": 2,
                "line_total_cents": 850,
            }
        ],
        "total_cents": 850,
    }

    incremented = client.post(
        "/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 1}
    )
    assert incremented.json()["items"][0]["quantity"] == 3
    assert incremented.json()["total_cents"] == 1275

    changed = client.put(
        f"/cart/items/{PRODUCT}", headers=SHOPPER, json={"quantity": 5}
    )
    assert changed.json()["items"][0]["quantity"] == 5
    assert changed.json()["total_cents"] == 2125

    removed = client.delete(f"/cart/items/{PRODUCT}", headers=SHOPPER)
    assert removed.status_code == 204
    assert client.get("/cart", headers=SHOPPER).json() == {"items": [], "total_cents": 0}


def test_overlapping_adds_preserve_both_quantity_increments(client, database, monkeypatch):
    client.post(
        "/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 1}
    )
    original_read = cart.read_cart_quantity
    both_have_read = Barrier(2, timeout=3)

    def synchronized_read(connection, cart_id, product_id):
        quantity = original_read(connection, cart_id, product_id)
        try:
            both_have_read.wait()
        except BrokenBarrierError:
            pass
        return quantity

    monkeypatch.setattr(cart, "read_cart_quantity", synchronized_read)

    def add_one():
        with TestClient(app) as concurrent_client:
            return concurrent_client.post(
                "/cart/items", headers=SHOPPER,
                json={"product_id": PRODUCT, "quantity": 1},
            )

    with ThreadPoolExecutor(max_workers=2) as executor:
        responses = list(executor.map(lambda _: add_one(), range(2)))
    with closing(connect(database)) as connection:
        quantity = connection.execute(
            """SELECT ci.quantity FROM cart_items ci JOIN carts c ON c.id = ci.cart_id
               WHERE c.user_id = ? AND ci.product_id = ?""",
            ("shopper-river", PRODUCT),
        ).fetchone()[0]

    assert ([response.status_code for response in responses], quantity) == ([200, 200], 3)


@pytest.mark.parametrize("quantity", [0, -1, True])
def test_cart_rejects_nonpositive_or_noninteger_quantities(client, quantity):
    assert client.post(
        "/cart/items",
        headers=SHOPPER,
        json={"product_id": PRODUCT, "quantity": quantity},
    ).status_code == 422
    assert client.put(
        f"/cart/items/{PRODUCT}", headers=SHOPPER, json={"quantity": quantity}
    ).status_code == 422
    assert client.get("/cart", headers=SHOPPER).json() == {"items": [], "total_cents": 0}


def test_missing_products_and_cart_items_return_not_found(client):
    assert client.post(
        "/cart/items", headers=SHOPPER, json={"product_id": "missing-product", "quantity": 1}
    ).status_code == 404
    assert client.put(
        "/cart/items/missing-product", headers=SHOPPER, json={"quantity": 1}
    ).status_code == 404
    assert client.delete("/cart/items/missing-product", headers=SHOPPER).status_code == 404


def test_cart_rejects_quantities_over_available_stock_without_partial_write(client):
    client.put(
        f"/admin/products/{PRODUCT}",
        headers=ADMIN,
        json={"name": "Berry Bowl", "category": "food", "price_cents": 425, "stock": 2},
    )

    added = client.post(
        "/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 3}
    )
    changed = client.put(
        f"/cart/items/{PRODUCT}", headers=SHOPPER, json={"quantity": 3}
    )

    assert added.status_code == changed.status_code == 409
    assert added.json() == changed.json() == {"detail": "Requested quantity exceeds available stock"}
    assert client.get("/cart", headers=SHOPPER).json() == {"items": [], "total_cents": 0}


def test_cart_uses_current_product_price(client):
    client.post("/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 2})
    client.put(
        f"/admin/products/{PRODUCT}",
        headers=ADMIN,
        json={"name": "Berry Bowl", "category": "food", "price_cents": 500, "stock": 12},
    )

    cart = client.get("/cart", headers=SHOPPER).json()

    assert cart["items"][0]["price_cents"] == 500
    assert cart["items"][0]["line_total_cents"] == 1000
    assert cart["total_cents"] == 1000


def test_each_shopper_has_an_independent_cart(client, database):
    with closing(connect(database)) as connection:
        connection.execute(
            "INSERT INTO users (id, name, role) VALUES (?, ?, ?)",
            ("shopper-lagoon", "Lani Lagoon", "shopper"),
        )
        connection.commit()

    second_shopper = {"X-User-Id": "shopper-lagoon"}
    client.post("/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 2})
    client.post("/cart/items", headers=second_shopper, json={"product_id": PRODUCT, "quantity": 1})

    assert client.get("/cart", headers=SHOPPER).json()["items"][0]["quantity"] == 2
    assert client.get("/cart", headers=second_shopper).json()["items"][0]["quantity"] == 1


def test_admin_unknown_and_unselected_users_cannot_access_shopper_cart(client):
    assert client.get("/cart").status_code == 401
    assert client.get("/cart", headers={"X-User-Id": "missing-user"}).status_code == 401
    assert client.get("/cart", headers=ADMIN).status_code == 403
    assert client.post(
        "/cart/items", headers=ADMIN, json={"product_id": PRODUCT, "quantity": 1}
    ).status_code == 403
    assert client.get("/cart", headers=SHOPPER).json() == {"items": [], "total_cents": 0}


def test_cart_survives_reopening_the_app_with_the_same_database(database):
    with TestClient(app) as first_app:
        first_app.post(
            "/cart/items", headers=SHOPPER, json={"product_id": PRODUCT, "quantity": 3}
        )

    with TestClient(app) as restarted_app:
        cart = restarted_app.get("/cart", headers=SHOPPER).json()

    assert cart["items"][0]["quantity"] == 3
    assert cart["total_cents"] == 1275
