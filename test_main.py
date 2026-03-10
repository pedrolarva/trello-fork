
import pytest
from fastapi.testclient import TestClient
from main import app, db, AddressInDB
import uuid

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    """Fixture to clear the database before each test."""
    db.clear()
    yield
    db.clear()

def test_create_address():
    response = client.post(
        "/addresses/",
        json={
            "street": "Rua Teste",
            "number": "123",
            "complement": "Apto 1",
            "neighborhood": "Bairro Teste",
            "city": "Cidade Teste",
            "state": "TS",
            "zip_code": "00000-000"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["street"] == "Rua Teste"
    assert "id" in data
    assert len(db) == 1
    assert db[0].street == "Rua Teste"

def test_create_address_invalid_zip_code():
    response = client.post(
        "/addresses/",
        json={
            "street": "Rua Teste",
            "number": "123",
            "complement": "Apto 1",
            "neighborhood": "Bairro Teste",
            "city": "Cidade Teste",
            "state": "TS",
            "zip_code": "00000"
        },
    )
    assert response.status_code == 422 # Unprocessable Entity for validation error

def test_read_addresses_empty():
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert response.json() == []

def test_read_addresses_with_data():
    address_in_db = AddressInDB(
        street="Rua Existente",
        number="456",
        neighborhood="Bairro Existente",
        city="Cidade Existente",
        state="EX",
        zip_code="99999-999"
    )
    db.append(address_in_db)
    response = client.get("/addresses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["street"] == "Rua Existente"
    assert data[0]["id"] == str(address_in_db.id)

def test_read_address_by_id():
    address_in_db = AddressInDB(
        street="Rua para Busca",
        number="789",
        neighborhood="Bairro Busca",
        city="Cidade Busca",
        state="BS",
        zip_code="11111-111"
    )
    db.append(address_in_db)
    response = client.get(f"/addresses/{address_in_db.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["street"] == "Rua para Busca"
    assert data["id"] == str(address_in_db.id)

def test_read_address_not_found():
    response = client.get(f"/addresses/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Address not found"}

def test_update_address():
    address_in_db = AddressInDB(
        street="Rua Antiga",
        number="100",
        neighborhood="Bairro Antigo",
        city="Cidade Antiga",
        state="MG",
        zip_code="30000-000"
    )
    db.append(address_in_db)
    response = client.put(
        f"/addresses/{address_in_db.id}",
        json={"street": "Rua Nova", "complement": "Nova Complemento"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["street"] == "Rua Nova"
    assert data["complement"] == "Nova Complemento"
    assert data["number"] == "100" # Should remain unchanged if not provided
    assert db[0].street == "Rua Nova"
    assert db[0].complement == "Nova Complemento"

def test_update_address_not_found():
    response = client.put(
        f"/addresses/{uuid.uuid4()}",
        json={"street": "Rua Inexistente"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Address not found"}

def test_delete_address():
    address_in_db = AddressInDB(
        street="Rua para Deletar",
        number="500",
        neighborhood="Bairro Deletar",
        city="Cidade Deletar",
        state="RJ",
        zip_code="20000-000"
    )
    db.append(address_in_db)
    response = client.delete(f"/addresses/{address_in_db.id}")
    assert response.status_code == 204
    assert len(db) == 0

def test_delete_address_not_found():
    response = client.delete(f"/addresses/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Address not found"}

