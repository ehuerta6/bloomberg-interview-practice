import asyncio
from contextlib import closing

import httpx
import pytest
from fastapi.testclient import TestClient

from app.db import PRODUCTS, connect, reset, seed
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "catalog.sqlite3"
    monkeypatch.setenv("CAPPY_DB_PATH", str(database))
    with closing(connect(database)) as connection:
        seed(connection)
    with TestClient(app) as test_client:
        yield test_client


def test_shoppers_can_list_and_read_seeded_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": product_id,
            "name": name,
            "category": category,
            "price_cents": price,
            "stock": stock,
        }
        for product_id, name, category, price, stock in sorted(PRODUCTS)
    ]
    assert client.get("/products/food-berry-bowl").json() == response.json()[0]


def test_unknown_product_returns_predictable_not_found(client):
    response = client.get("/products/missing-product")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
    assert client.put(
        "/admin/products/missing-product",
        headers={"X-User-Id": "admin-stone"},
        json={"name": "Missing", "category": "toys", "price_cents": 10, "stock": 1},
    ).status_code == 404


def test_admin_can_create_update_and_cannot_create_duplicates(client):
    headers = {"X-User-Id": "admin-stone"}
    product = {
        "id": "toy-reed-boat",
        "name": "Reed Boat",
        "category": "toys",
        "price_cents": 550,
        "stock": 3,
    }

    created = client.post("/admin/products", headers=headers, json=product)
    assert created.status_code == 201
    assert created.headers["location"] == "/products/toy-reed-boat"
    assert created.json() == product
    assert client.post("/admin/products", headers=headers, json=product).status_code == 409

    updated = {"name": "Tiny Reed Boat", "category": "toys", "price_cents": 625, "stock": 7}
    response = client.put("/admin/products/toy-reed-boat", headers=headers, json=updated)

    assert response.status_code == 200
    assert response.json() == {"id": "toy-reed-boat", **updated}
    assert client.get("/products/toy-reed-boat").json() == response.json()


@pytest.mark.parametrize(
    "override",
    [
        {"id": "bad id"},
        {"name": ""},
        {"name": "   "},
        {"category": "snacks"},
        {"price_cents": -1},
        {"price_cents": 2**63},
        {"stock": -1},
        {"stock": True},
        {"unexpected": "field"},
    ],
)
def test_admin_rejects_invalid_product_details(client, override):
    product = {
        "id": "toy-reed-boat",
        "name": "Reed Boat",
        "category": "toys",
        "price_cents": 550,
        "stock": 3,
    }
    product.update(override)

    response = client.post(
        "/admin/products", headers={"X-User-Id": "admin-stone"}, json=product
    )

    assert response.status_code == 422
    assert client.get("/products/toy-reed-boat").status_code == 404


def test_shopper_and_unselected_users_cannot_modify_products(client):
    product = {
        "id": "toy-reed-boat",
        "name": "Reed Boat",
        "category": "toys",
        "price_cents": 550,
        "stock": 3,
    }
    update = {"name": "Changed", "category": "toys", "price_cents": 1, "stock": 0}
    original = client.get("/products/food-berry-bowl").json()

    assert client.post(
        "/admin/products", headers={"X-User-Id": "shopper-river"}, json=product
    ).status_code == 403
    assert client.put(
        "/admin/products/food-berry-bowl",
        headers={"X-User-Id": "shopper-river"},
        json=update,
    ).status_code == 403
    assert client.post("/admin/products", json=product).status_code == 401
    assert client.get("/products/food-berry-bowl").json() == original
    assert client.get("/products/toy-reed-boat").status_code == 404


def test_reset_restores_deterministic_seeded_catalog(client, tmp_path, monkeypatch):
    database = tmp_path / "catalog.sqlite3"
    monkeypatch.setenv("CAPPY_DB_PATH", str(database))
    original = client.get("/products").json()
    headers = {"X-User-Id": "admin-stone"}

    client.put(
        "/admin/products/food-berry-bowl",
        headers=headers,
        json={"name": "Altered Bowl", "category": "food", "price_cents": 1, "stock": 0},
    )
    client.post(
        "/admin/products",
        headers=headers,
        json={"id": "toy-extra", "name": "Extra", "category": "toys", "price_cents": 3, "stock": 9},
    )

    with closing(connect(database)) as connection:
        reset(connection)

    assert client.get("/products").json() == original


def test_concurrent_catalog_requests_work_across_api_workers(client):
    async def fetch_catalogs():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
            return await asyncio.gather(
                *(async_client.get("/products") for _ in range(24))
            )

    responses = asyncio.run(fetch_catalogs())

    assert all(response.status_code == 200 for response in responses)
    assert all(len(response.json()) == len(PRODUCTS) for response in responses)
