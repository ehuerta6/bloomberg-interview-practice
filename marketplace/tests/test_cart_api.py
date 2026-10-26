from contextlib import closing

import pytest
from fastapi.testclient import TestClient

from app.db import connect, seed
from app.main import app


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
