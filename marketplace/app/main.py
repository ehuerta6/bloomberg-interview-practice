import sqlite3
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.admin import router as admin_router
from app.cart import router as cart_router
from app.checkout import router as checkout_router
from app.dependencies import get_connection, require_admin
from app.orders import router as orders_router

app = FastAPI(title="Cappy Marketplace")

ProductCategory = Literal["food", "stones", "sticks", "toys"]
ProductName = Annotated[
    str, StringConstraints(min_length=1, max_length=120, strip_whitespace=True)
]


class ProductInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name: ProductName
    category: ProductCategory
    price_cents: int = Field(strict=True, ge=0, le=2**63 - 1)
    stock: int = Field(strict=True, ge=0, le=2**63 - 1)


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: ProductName
    category: ProductCategory
    price_cents: int = Field(strict=True, ge=0, le=2**63 - 1)
    stock: int = Field(strict=True, ge=0, le=2**63 - 1)


def product_dict(row: sqlite3.Row) -> dict[str, str | int]:
    return {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price_cents": row["price_cents"],
        "stock": row["stock"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products")
def list_products(
    connection: sqlite3.Connection = Depends(get_connection),
) -> list[dict[str, str | int]]:
    rows = connection.execute(
        "SELECT id, name, category, price_cents, stock FROM products ORDER BY id"
    ).fetchall()
    return [product_dict(row) for row in rows]


@app.get("/products/{product_id}")
def get_product(
    product_id: str, connection: sqlite3.Connection = Depends(get_connection)
) -> dict[str, str | int]:
    row = connection.execute(
        "SELECT id, name, category, price_cents, stock FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_dict(row)


@app.post("/admin/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductInput,
    response: Response,
    _admin_user_id: str = Depends(require_admin),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, str | int]:
    try:
        with connection:
            connection.execute(
                """INSERT INTO products (id, name, category, price_cents, stock)
                   VALUES (:id, :name, :category, :price_cents, :stock)""",
                product.model_dump(),
            )
    except sqlite3.IntegrityError as error:
        if connection.execute("SELECT 1 FROM products WHERE id = ?", (product.id,)).fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Product already exists"
            ) from error
        raise
    response.headers["Location"] = f"/products/{product.id}"
    return product.model_dump()


@app.put("/admin/products/{product_id}")
def update_product(
    product_id: str,
    product: ProductUpdate,
    _admin_user_id: str = Depends(require_admin),
    connection: sqlite3.Connection = Depends(get_connection),
) -> dict[str, str | int]:
    with connection:
        cursor = connection.execute(
            """UPDATE products
               SET name = :name, category = :category,
                   price_cents = :price_cents, stock = :stock
               WHERE id = :id""",
            product.model_dump() | {"id": product_id},
        )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"id": product_id, **product.model_dump()}


app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(orders_router)
app.include_router(admin_router)
STATIC_DIRECTORY = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
def marketplace_page() -> FileResponse:
    return FileResponse(STATIC_DIRECTORY / "index.html")


app.mount("/assets", StaticFiles(directory=STATIC_DIRECTORY), name="frontend-assets")
