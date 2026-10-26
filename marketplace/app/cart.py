"""Shopper cart API backed by the existing SQLite cart tables."""

import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

from app.dependencies import get_connection, require_shopper

router = APIRouter(tags=["cart"])
CartId = Annotated[
    str,
    Field(min_length=1, max_length=80, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$"),
]
CartQuantity = Annotated[int, Field(strict=True, gt=0, le=2**63 - 1)]


class AddCartItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: CartId
    quantity: CartQuantity


class SetCartQuantity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: CartQuantity


def cart_snapshot(connection: sqlite3.Connection, user_id: str) -> dict[str, object]:
    rows = connection.execute(
        """SELECT p.id AS product_id, p.name, p.category, p.price_cents, ci.quantity
           FROM carts c
           JOIN cart_items ci ON ci.cart_id = c.id
           JOIN products p ON p.id = ci.product_id
           WHERE c.user_id = ?
           ORDER BY p.id""",
        (user_id,),
    ).fetchall()
    items = [
        {
            "product_id": row["product_id"],
            "name": row["name"],
            "category": row["category"],
            "price_cents": row["price_cents"],
            "quantity": row["quantity"],
            "line_total_cents": row["price_cents"] * row["quantity"],
        }
        for row in rows
    ]
    return {
        "items": items,
        "total_cents": sum(item["line_total_cents"] for item in items),
    }


def get_or_create_cart_id(connection: sqlite3.Connection, user_id: str) -> int:
    cart = connection.execute(
        "SELECT id FROM carts WHERE user_id = ?", (user_id,)
    ).fetchone()
    if cart is not None:
        return cart["id"]
    cursor = connection.execute("INSERT INTO carts (user_id) VALUES (?)", (user_id,))
    return cursor.lastrowid


def save_quantity(
    connection: sqlite3.Connection,
    user_id: str,
    product_id: str,
    quantity: int,
    *,
    add_to_existing: bool,
) -> None:
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        product = connection.execute(
            "SELECT stock FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        cart_id = get_or_create_cart_id(connection, user_id)
        current = connection.execute(
            "SELECT quantity FROM cart_items WHERE cart_id = ? AND product_id = ?",
            (cart_id, product_id),
        ).fetchone()
        desired_quantity = quantity
        if add_to_existing and current is not None:
            desired_quantity += current["quantity"]
        if desired_quantity > product["stock"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Requested quantity exceeds available stock",
            )

        connection.execute(
            """INSERT INTO cart_items (cart_id, product_id, quantity)
               VALUES (?, ?, ?)
               ON CONFLICT (cart_id, product_id)
               DO UPDATE SET quantity = excluded.quantity""",
            (cart_id, product_id, desired_quantity),
        )


@router.get("/cart")
def get_cart(
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, object]:
    return cart_snapshot(connection, user_id)


@router.post("/cart/items")
def add_cart_item(
    item: AddCartItem,
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, object]:
    save_quantity(
        connection,
        user_id,
        item.product_id,
        item.quantity,
        add_to_existing=True,
    )
    return cart_snapshot(connection, user_id)


@router.put("/cart/items/{product_id}")
def set_cart_item_quantity(
    product_id: str,
    item: SetCartQuantity,
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, object]:
    save_quantity(
        connection,
        user_id,
        product_id,
        item.quantity,
        add_to_existing=False,
    )
    return cart_snapshot(connection, user_id)


@router.delete("/cart/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    product_id: str,
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> Response:
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        cart = connection.execute(
            "SELECT id FROM carts WHERE user_id = ?", (user_id,)
        ).fetchone()
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
            )
        cursor = connection.execute(
            "DELETE FROM cart_items WHERE cart_id = ? AND product_id = ?",
            (cart["id"], product_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
            )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
