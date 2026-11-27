from fastapi.testclient import TestClient

from app.main import app, items_db

client = TestClient(app)


def setup_function() -> None:
    """Limpia la lista en memoria antes de cada test."""
    items_db.clear()


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_list_items_empty() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_list_item() -> None:
    payload = {"name": "Teclado mecánico", "price": 59.99}
    post_res = client.post("/items", json=payload)
    assert post_res.status_code == 201
    data = post_res.json()
    assert data["id"] == 1
    assert data["name"] == "Teclado mecánico"
    assert data["price"] == 59.99

    get_res = client.get("/items")
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1


def test_create_item_invalid_price() -> None:
    response = client.post("/items", json={"name": "Error", "price": -5})
    assert response.status_code == 422