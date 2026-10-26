"""Transactional fake-payment checkout API."""

import sqlite3
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from app.dependencies import get_connection, require_shopper

router = APIRouter(tags=["checkout"])
PaymentOutcome = Literal["success", "decline", "temporary_error"]
SQLITE_MAX_INTEGER = 2**63 - 1


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment_outcome: PaymentOutcome = "success"


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


def save_attempt(
    connection: sqlite3.Connection,
    user_id: str,
    idempotency_key: str,
    payment_outcome: str,
    status_code: int,
    *,
    detail: str | None = None,
    order_id: int | None = None,
) -> None:
    connection.execute(
        """INSERT OR IGNORE INTO checkout_attempts
           (user_id, idempotency_key, payment_outcome, status_code, detail, order_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, idempotency_key, payment_outcome, status_code, detail, order_id),
    )


def replay_attempt(
    connection: sqlite3.Connection, attempt: sqlite3.Row
) -> JSONResponse:
    if attempt["order_id"] is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=order_snapshot(connection, attempt["order_id"]),
        )
    return JSONResponse(
        status_code=attempt["status_code"], content={"detail": attempt["detail"]}
    )


@router.post("/checkout")
def checkout(
    request: CheckoutRequest,
    idempotency_key: Annotated[
        str, Header(alias="Idempotency-Key", min_length=1, max_length=128)
    ],
    user_id: str = Depends(require_shopper),
    connection: sqlite3.Connection = Depends(get_connection),
) -> JSONResponse:
    idempotency_key = idempotency_key.strip()
    if not idempotency_key:
        raise HTTPException(
            status_code=422,
            detail="Idempotency-Key must not be blank",
        )

    with connection:
        previous = connection.execute(
            """SELECT payment_outcome, status_code, detail, order_id
               FROM checkout_attempts WHERE user_id = ? AND idempotency_key = ?""",
            (user_id, idempotency_key),
        ).fetchone()
        if previous is not None:
            if previous["payment_outcome"] != request.payment_outcome:
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={
                        "detail": "Idempotency key already used with a different payment outcome"
                    },
                )
            return replay_attempt(connection, previous)

        cart = connection.execute(
            "SELECT id FROM carts WHERE user_id = ?", (user_id,)
        ).fetchone()
        if cart is None:
            save_attempt(
                connection,
                user_id,
                idempotency_key,
                request.payment_outcome,
                status.HTTP_409_CONFLICT,
                detail="Cart is empty",
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT, content={"detail": "Cart is empty"}
            )

        items = connection.execute(
            """SELECT p.id AS product_id, p.name, p.category, p.price_cents,
                      p.stock, ci.quantity
               FROM cart_items ci
               JOIN products p ON p.id = ci.product_id
               WHERE ci.cart_id = ? ORDER BY p.id""",
            (cart["id"],),
        ).fetchall()
        connection.execute("BEGIN IMMEDIATE")
        if not items:
            save_attempt(
                connection,
                user_id,
                idempotency_key,
                request.payment_outcome,
                status.HTTP_409_CONFLICT,
                detail="Cart is empty",
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT, content={"detail": "Cart is empty"}
            )

        total_cents = 0
        order_items: list[dict[str, str | int]] = []
        for item in items:
            if item["quantity"] > item["stock"]:
                detail = "Insufficient stock"
                save_attempt(
                    connection,
                    user_id,
                    idempotency_key,
                    request.payment_outcome,
                    status.HTTP_409_CONFLICT,
                    detail=detail,
                )
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT, content={"detail": detail}
                )
            line_total = item["price_cents"] * item["quantity"]
            if line_total > SQLITE_MAX_INTEGER or total_cents + line_total > SQLITE_MAX_INTEGER:
                detail = "Order total exceeds supported range"
                save_attempt(
                    connection,
                    user_id,
                    idempotency_key,
                    request.payment_outcome,
                    status.HTTP_409_CONFLICT,
                    detail=detail,
                )
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT, content={"detail": detail}
                )
            total_cents += line_total
            order_items.append(
                {
                    "product_id": item["product_id"],
                    "product_name": item["name"],
                    "category": item["category"],
                    "price_cents": item["price_cents"],
                    "quantity": item["quantity"],
                    "line_total_cents": line_total,
                }
            )

        if request.payment_outcome == "decline":
            detail = "Payment declined"
            save_attempt(
                connection,
                user_id,
                idempotency_key,
                request.payment_outcome,
                status.HTTP_402_PAYMENT_REQUIRED,
                detail=detail,
            )
            return JSONResponse(
                status_code=status.HTTP_402_PAYMENT_REQUIRED, content={"detail": detail}
            )
        if request.payment_outcome == "temporary_error":
            detail = "Temporary payment error"
            save_attempt(
                connection,
                user_id,
                idempotency_key,
                request.payment_outcome,
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=detail,
            )
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": detail},
            )

        order_cursor = connection.execute(
            "INSERT INTO orders (user_id, status, total_cents) VALUES (?, 'placed', ?)",
            (user_id, total_cents),
        )
        order_id = order_cursor.lastrowid
        for item in order_items:
            updated = connection.execute(
                """UPDATE products SET stock = stock - ?
                   WHERE id = ? AND stock >= ?""",
                (item["quantity"], item["product_id"], item["quantity"]),
            )
            if updated.rowcount != 1:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Insufficient stock"
                )
            connection.execute(
                """INSERT INTO order_items
                   (order_id, product_id, product_name, category, price_cents,
                    quantity, line_total_cents)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    order_id,
                    item["product_id"],
                    item["product_name"],
                    item["category"],
                    item["price_cents"],
                    item["quantity"],
                    item["line_total_cents"],
                ),
            )
        connection.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart["id"],))
        save_attempt(
            connection,
            user_id,
            idempotency_key,
            request.payment_outcome,
            status.HTTP_201_CREATED,
            order_id=order_id,
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=order_snapshot(connection, order_id),
    )
