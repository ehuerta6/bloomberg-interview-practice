from contextlib import closing

from fastapi.testclient import TestClient
import pytest

from app.db import connect, seed
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "frontend.sqlite3"
    monkeypatch.setenv("CAPPY_DB_PATH", str(database))
    with closing(connect(database)) as connection:
        seed(connection)
    with TestClient(app) as test_client:
        yield test_client


def test_marketplace_serves_frontend_assets_and_keeps_api_routes_available(client):
    page = client.get("/")

    assert page.status_code == 200
    assert "Cappy Cove" in page.text
    assert 'aria-label="Marketplace sections"' in page.text
    assert 'id="identity-select"' in page.text
    assert client.get("/assets/styles.css").status_code == 200
    script = client.get("/assets/app.js")
    assert script.status_code == 200
    assert '"/checkout"' in script.text
    assert client.get("/products").json()[0]["id"] == "food-berry-bowl"
    assert client.post("/admin/orders/unknown/cancel").status_code == 404
