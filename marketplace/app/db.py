"""SQLite setup and deterministic local fixture data."""

from __future__ import annotations

import argparse
import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("data/cappy.sqlite3")

USERS = (
    ("shopper-river", "Riley River", "shopper"),
    ("admin-stone", "Sage Stone", "admin"),
)

PRODUCTS = (
    ("food-berry-bowl", "Berry Bowl", "food", 425, 12),
    ("stone-smooth-river-stone", "Smooth River Stone", "stones", 275, 8),
    ("stick-willow-wand", "Willow Wand", "sticks", 150, 16),
    ("toy-floating-duck", "Floating Duck", "toys", 899, 5),
)

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('shopper', 'admin'))
);
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0)
);
CREATE TABLE IF NOT EXISTS carts (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS cart_items (
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (cart_id, product_id)
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL REFERENCES users(id),
    status TEXT NOT NULL DEFAULT 'placed',
    total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    line_total_cents INTEGER NOT NULL CHECK (line_total_cents >= 0),
    PRIMARY KEY (order_id, product_id)
);
CREATE TABLE IF NOT EXISTS checkout_attempts (
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    idempotency_key TEXT NOT NULL,
    payment_outcome TEXT NOT NULL CHECK (
        payment_outcome IN ('success', 'decline', 'temporary_error')
    ),
    status_code INTEGER NOT NULL CHECK (status_code BETWEEN 200 AND 599),
    detail TEXT,
    order_id INTEGER REFERENCES orders(id),
    PRIMARY KEY (user_id, idempotency_key),
    CHECK (
        (order_id IS NULL AND detail IS NOT NULL)
        OR (order_id IS NOT NULL AND detail IS NULL)
    )
);
"""


def database_path() -> Path:
    """Resolve the local DB path, allowing tests and contributors to override it."""
    return Path(os.environ.get("CAPPY_DB_PATH", DEFAULT_DB_PATH))


def connect(
    path: Path | None = None, *, check_same_thread: bool = True
) -> sqlite3.Connection:
    db_path = path or database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, check_same_thread=check_same_thread)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA)


def seed(connection: sqlite3.Connection) -> None:
    """Insert fixture rows once, making repeated setup safe."""
    initialize(connection)
    with connection:
        connection.executemany(
            "INSERT OR IGNORE INTO users (id, name, role) VALUES (?, ?, ?)", USERS
        )
        connection.executemany(
            """INSERT OR IGNORE INTO products
               (id, name, category, price_cents, stock) VALUES (?, ?, ?, ?, ?)""",
            PRODUCTS,
        )
        connection.executemany(
            "INSERT OR IGNORE INTO carts (user_id) VALUES (?)",
            ((user_id,) for user_id, _, role in USERS if role == "shopper"),
        )


def reset(connection: sqlite3.Connection) -> None:
    """Restore the database to the exact initial fixture state."""
    with connection:
        connection.execute("DELETE FROM checkout_attempts")
        connection.execute("DELETE FROM orders")
        connection.execute("DELETE FROM sqlite_sequence WHERE name = 'orders'")
        connection.execute("DELETE FROM cart_items")
        connection.execute("DELETE FROM carts")
        connection.execute("DELETE FROM products")
        connection.execute("DELETE FROM users")
    seed(connection)


def run(command: str, path: Path | None = None) -> None:
    with connect(path) as connection:
        if command == "seed":
            seed(connection)
        elif command == "reset":
            initialize(connection)
            reset(connection)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the local Cappy Marketplace database")
    parser.add_argument("command", choices=("seed", "reset"))
    args = parser.parse_args()
    run(args.command)
    print(f"Database {args.command} complete: {database_path()}")


if __name__ == "__main__":
    main()
