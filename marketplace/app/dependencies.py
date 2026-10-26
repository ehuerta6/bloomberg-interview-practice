"""Shared FastAPI dependencies for local database access."""

from collections.abc import Iterator
import sqlite3
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from app.db import connect


def get_connection() -> Iterator[sqlite3.Connection]:
    # FastAPI may hand a sync dependency and its route to different workers.
    connection = connect(check_same_thread=False)
    try:
        yield connection
    finally:
        connection.close()


def require_shopper(
    user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    connection: sqlite3.Connection = Depends(get_connection),
) -> str:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Select a local user"
        )
    user = connection.execute(
        "SELECT role FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown local user"
        )
    if user["role"] != "shopper":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Shopper access required"
        )
    return user_id


def require_admin(
    user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    connection: sqlite3.Connection = Depends(get_connection),
) -> str:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Select a local user"
        )
    user = connection.execute(
        "SELECT role FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown local user"
        )
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return user_id
