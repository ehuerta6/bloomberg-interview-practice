import os
import sqlite3
import subprocess
import sys

import pytest

from app.db import PRODUCTS, USERS, connect, reset, seed


@pytest.fixture
def connection(tmp_path):
    conn = connect(tmp_path / "market.sqlite3")
    try:
        yield conn
    finally:
        conn.close()


def rows(connection, table):
    return [tuple(row) for row in connection.execute(f"SELECT * FROM {table} ORDER BY 1")]


def test_seed_is_repeatable_and_creates_empty_shopper_carts(connection):
    seed(connection)
    first = {table: rows(connection, table) for table in ("users", "products", "carts", "cart_items")}
    seed(connection)
    second = {table: rows(connection, table) for table in first}

    assert first == second
    assert len(first["users"]) == len(USERS)
    assert len(first["products"]) == len(PRODUCTS)
    assert len(first["carts"]) == 1
    assert first["cart_items"] == []


def test_reset_restores_fixture_data_and_clears_persisted_cart_state(connection):
    seed(connection)
    connection.execute("INSERT INTO cart_items VALUES (1, ?, 3)", (PRODUCTS[0][0],))
    connection.execute("UPDATE products SET stock = 0 WHERE id = ?", (PRODUCTS[0][0],))
    connection.execute("UPDATE users SET name = 'Changed' WHERE id = ?", (USERS[0][0],))
    connection.commit()

    reset(connection)

    assert [tuple(row) for row in connection.execute(
        "SELECT id, name, role FROM users ORDER BY id"
    )] == sorted(USERS)
    assert [tuple(row) for row in connection.execute(
        "SELECT id, name, category, price_cents, stock FROM products ORDER BY id"
    )] == sorted(PRODUCTS)
    assert connection.execute("SELECT COUNT(*) FROM carts").fetchone()[0] == 1
    assert connection.execute("SELECT COUNT(*) FROM cart_items").fetchone()[0] == 0


def test_database_enforces_positive_cart_quantity(connection):
    seed(connection)
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute("INSERT INTO cart_items VALUES (1, ?, 0)", (PRODUCTS[0][0],))


def test_seed_and_reset_cli_work_against_a_fresh_database(tmp_path):
    database = tmp_path / "fresh.sqlite3"
    environment = os.environ | {"CAPPY_DB_PATH": str(database)}
    for command in ("seed", "seed", "reset"):
        subprocess.run(
            [sys.executable, "-m", "app.db", command],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )

    with connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == len(USERS)
        assert connection.execute("SELECT COUNT(*) FROM products").fetchone()[0] == len(PRODUCTS)
        assert connection.execute("SELECT COUNT(*) FROM carts").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM cart_items").fetchone()[0] == 0
