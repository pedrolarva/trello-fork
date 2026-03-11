import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.address_repository import address_repo
import uuid

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    address_repo._db = []
    yield
    address_repo._db = []

def test_create_address():
    payload = {
        "street": "Rua da Consolação",
        "number": "123",
        "neighborhood": "Centro",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01301-100"
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["street"] == payload["street"]
    assert "id" in data

def test_list_addresses():
    client.post("/addresses/", json={
        "street": "Rua A", "number": "1", "neighborhood": "B", "city": "C", "state": "SP", "zip_code": "12345-678"
    })
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_address():
    create_resp = client.post("/addresses/", json={
        "street": "Rua A", "number": "1", "neighborhood": "B", "city": "C", "state": "SP", "zip_code": "12345-678"
    })
    address_id = create_resp.json()["id"]
    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 200
    assert response.json()["id"] == address_id

def test_update_address():
    create_resp = client.post("/addresses/", json={
        "street": "Rua A", "number": "1", "neighborhood": "B", "city": "C", "state": "SP", "zip_code": "12345-678"
    })
    address_id = create_resp.json()["id"]
    response = client.put(f"/addresses/{address_id}", json={"street": "Rua B"})
    assert response.status_code == 200
    assert response.json()["street"] == "Rua B"

def test_delete_address():
    create_resp = client.post("/addresses/", json={
        "street": "Rua A", "number": "1", "neighborhood": "B", "city": "C", "state": "SP", "zip_code": "12345-678"
    })
    address_id = create_resp.json()["id"]
    response = client.delete(f"/addresses/{address_id}")
    assert response.status_code == 204
    assert len(client.get("/addresses/").json()) == 0

def test_address_not_found():
    random_id = str(uuid.uuid4())
    assert client.get(f"/addresses/{random_id}").status_code == 404
    assert client.put(f"/addresses/{random_id}", json={"street": "X"}).status_code == 404
    assert client.delete(f"/addresses/{random_id}").status_code == 404

def test_invalid_zip_code():
    payload = {
        "street": "Rua da Consolação",
        "number": "123",
        "neighborhood": "Centro",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01301100" # Missing hyphen
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 422
