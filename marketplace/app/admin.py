"""Read-only order inspection and validated inventory adjustments for admins."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.dependencies import get_connection, require_admin

router = APIRouter(dependencies=[Depends(require_admin)])
MAX_INTEGER = 2**63 - 1


class StockAdjustment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    delta: int = Field(strict=True, ge=-MAX_INTEGER, le=MAX_INTEGER)

    @field_validator("delta")
    @classmethod
    def require_nonzero_delta(cls, value: int) -> int:
        if value == 0:
            raise ValueError("delta must not be zero")
        return value


@router.get("/admin/orders")
def list_orders(
    connection: sqlite3.Connection = Depends(get_connection),
) -> list[dict[str, object]]:
    orders = connection.execute(
        """SELECT id, user_id, status, total_cents, created_at
           FROM orders ORDER BY id"""
    ).fetchall()
    result = []
    for order in orders:
        items = connection.execute(
            """SELECT product_id, product_name, category, price_cents,
                      quantity, line_total_cents
               FROM order_items WHERE order_id = ? ORDER BY product_id""",
            (order["id"],),
        ).fetchall()
        result.append(
            {
                "id": order["id"],
                "user_id": order["user_id"],
                "status": order["status"],
                "total_cents": order["total_cents"],
                "created_at": order["created_at"],
                "items": [
                    {
                        "product_id": item["product_id"],
                        "name": item["product_name"],
                        "category": item["category"],
                        "price_cents": item["price_cents"],
                        "quantity": item["quantity"],
                        "line_total_cents": item["line_total_cents"],
                    }
                    for item in items
                ],
            }
        )
    return result


@router.post("/admin/products/{product_id}/stock-adjustments")
def adjust_stock(
    product_id: str,
    adjustment: StockAdjustment,
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, int | str]:
    connection.execute("BEGIN IMMEDIATE")
    try:
        product = connection.execute(
            "SELECT stock FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        new_stock = product["stock"] + adjustment.delta
        if not 0 <= new_stock <= MAX_INTEGER:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Stock adjustment would exceed valid stock",
            )
        connection.execute(
            "UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id)
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return {"product_id": product_id, "delta": adjustment.delta, "stock": new_stock}
