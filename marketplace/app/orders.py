"""Shopper order history and transactional cancellation API."""

import sqlite3
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_connection, require_shopper

router = APIRouter(tags=["orders"])
SQLITE_MAX_INTEGER = 2**63 - 1


def order_snapshot(connection: sqlite3.Connection, order_id: int) -> dict[str, object]:
    order = connection.execute(
        "SELECT id, status, total_cents, created_at FROM orders WHERE id = ?",
        (order_id,),
    ).fetchone()
    items = connection.execute(
        """SELECT product_id, product_name AS name, category, price_cents,
                  quantity, line_total_cents
           FROM order_items WHERE order_id = ? ORDER BY product_id""",
        (order_id,),
    ).fetchall()
    return {
        "id": order["id"],
        "status": order["status"],
        "created_at": order["created_at"],
        "total_cents": order["total_cents"],
        "items": [dict(item) for item in items],
    }


def shopper_order(
    connection: sqlite3.Connection, order_id: int, user_id: str
) -> dict[str, Any]:
    order = connection.execute(
        "SELECT id FROM orders WHERE id = ? AND user_id = ?", (order_id, user_id)
    ).fetchone()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order_snapshot(connection, order_id)


@router.get("/orders")
def list_orders(
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> list[dict[str, object]]:
    rows = connection.execute(
        "SELECT id FROM orders WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    return [order_snapshot(connection, row["id"]) for row in rows]


@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, object]:
    return shopper_order(connection, order_id, user_id)


@router.post("/orders/{order_id}/cancel")
def cancel_order(
    order_id: int,
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, object]:
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        owned = connection.execute(
            "SELECT status FROM orders WHERE id = ? AND user_id = ?", (order_id, user_id)
        ).fetchone()
        if owned is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if owned["status"] != "placed":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only placed orders can be cancelled",
            )

        changed = connection.execute(
            """UPDATE orders SET status = 'cancelled'
               WHERE id = ? AND user_id = ? AND status = 'placed'""",
            (order_id, user_id),
        )
        if changed.rowcount != 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only placed orders can be cancelled",
            )

        items = connection.execute(
            "SELECT product_id, quantity FROM order_items WHERE order_id = ?", (order_id,)
        ).fetchall()
        for item in items:
            restored = connection.execute(
                """UPDATE products SET stock = stock + ?
                   WHERE id = ? AND stock <= ?""",
                (
                    item["quantity"],
                    item["product_id"],
                    SQLITE_MAX_INTEGER - item["quantity"],
                ),
            )
            if restored.rowcount != 1:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Order inventory could not be restored",
                )

    return order_snapshot(connection, order_id)
