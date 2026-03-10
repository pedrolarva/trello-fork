
import pytest
from fastapi.testclient import TestClient
from address_api.main import app
from address_api.models import db, next_id, Address

# Initialize the TestClient for the FastAPI application
client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Fixture to clear the database and reset the next_id before each test.
    This ensures that each test runs with a clean state.
    """
    global db
    global next_id
    db.clear()
    next_id = 1
    yield
    db.clear()
    next_id = 1


def test_create_address():
    """
    Test case for creating a new address.
    It should return a 201 status code and the created address details.
    """
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "90210",
        "country": "USA",
        "complement": "Apt 101",
        "number": "123A"
    }
    response = client.post("/addresses/", json=address_data)
    assert response.status_code == 201
    created_address = response.json()
    assert created_address["id"] == 1
    assert created_address["street"] == "123 Main St"
    assert "complement" in created_address
    assert "number" in created_address

def test_create_address_missing_required_field():
    """
    Test case for creating an address with a missing required field (e.g., street).
    It should return a 422 status code (Unprocessable Entity) due to validation error.
    """
    address_data = {
        "city": "Anytown",
        "state": "CA",
        "zip_code": "90210",
        "country": "USA"
    }
    response = client.post("/addresses/", json=address_data)
    assert response.status_code == 422
    assert "field_errors" in response.json()["detail"][0]

def test_create_address_invalid_zip_code():
    """
    Test case for creating an address with an invalid zip code format.
    It should return a 422 status code (Unprocessable Entity) due to validation error.
    """
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "123",  # Invalid format
        "country": "USA"
    }
    response = client.post("/addresses/", json=address_data)
    assert response.status_code == 422
    assert "field_errors" in response.json()["detail"][0]


def test_read_address():
    """
    Test case for reading an existing address by its ID.
    It should return a 200 status code and the address details.
    """
    # First, create an address to read
    address_data = {
        "street": "456 Oak Ave",
        "city": "Otherville",
        "state": "NY",
        "zip_code": "10001",
        "country": "USA"
    }
    create_response = client.post("/addresses/", json=address_data)
    created_id = create_response.json()["id"]

    # Now, read the created address
    response = client.get(f"/addresses/{created_id}")
    assert response.status_code == 200
    read_address = response.json()
    assert read_address["id"] == created_id
    assert read_address["street"] == "456 Oak Ave"

def test_read_non_existent_address():
    """
    Test case for reading a non-existent address.
    It should return a 404 status code (Not Found).
    """
    response = client.get("/addresses/999")  # ID 999 is unlikely to exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"

def test_read_address_invalid_id():
    """
    Test case for reading an address with an invalid ID (e.g., zero or negative).
    It should return a 422 status code (Unprocessable Entity).
    """
    response = client.get("/addresses/0")  # ID must be > 0
    assert response.status_code == 422

def test_read_all_addresses_empty():
    """
    Test case for reading all addresses when no addresses exist.
    It should return an empty list.
    """
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert response.json() == []

def test_read_all_addresses_multiple():
    """
    Test case for reading all addresses when multiple addresses exist.
    It should return a list of all addresses.
    """
    address_data_1 = {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "90210",
        "country": "USA"
    }
    address_data_2 = {
        "street": "456 Oak Ave",
        "city": "Otherville",
        "state": "NY",
        "zip_code": "10001",
        "country": "USA"
    }
    client.post("/addresses/", json=address_data_1)
    client.post("/addresses/", json=address_data_2)

    response = client.get("/addresses/")
    assert response.status_code == 200
    addresses = response.json()
    assert len(addresses) == 2
    assert addresses[0]["street"] == "123 Main St"
    assert addresses[1]["street"] == "456 Oak Ave"


def test_update_address_full():
    """
    Test case for fully updating an existing address.
    It should return a 200 status code and the updated address details.
    """
    # First, create an address
    address_data = {
        "street": "789 Pine Rd",
        "city": "Villagetown",
        "state": "TX",
        "zip_code": "77001",
        "country": "USA"
    }
    create_response = client.post("/addresses/", json=address_data)
    created_id = create_response.json()["id"]

    # Now, update the address
    update_data = {
        "street": "101 New Blvd",
        "city": "Metropolis",
        "state": "IL",
        "zip_code": "60601",
        "country": "USA",
        "complement": "Suite 500",
        "number": "101"
    }
    response = client.put(f"/addresses/{created_id}", json=update_data)
    assert response.status_code == 200
    updated_address = response.json()
    assert updated_address["id"] == created_id
    assert updated_address["street"] == "101 New Blvd"
    assert updated_address["city"] == "Metropolis"
    assert updated_address["zip_code"] == "60601"
    assert updated_address["complement"] == "Suite 500"
    assert updated_address["number"] == "101"


def test_update_address_partial():
    """
    Test case for partially updating an existing address.
    It should return a 200 status code and the partially updated address details.
    """
    # First, create an address
    address_data = {
        "street": "789 Pine Rd",
        "city": "Villagetown",
        "state": "TX",
        "zip_code": "77001",
        "country": "USA",
        "complement": "Apt 2B",
        "number": "789"
    }
    create_response = client.post("/addresses/", json=address_data)
    created_id = create_response.json()["id"]

    # Now, partially update the address
    partial_update_data = {
        "city": "Newtown",
        "zip_code": "77002-123",
        "complement": None  # Example of setting a field to None
    }
    response = client.put(f"/addresses/{created_id}", json=partial_update_data)
    assert response.status_code == 200
    updated_address = response.json()
    assert updated_address["id"] == created_id
    assert updated_address["street"] == "789 Pine Rd"  # Should remain unchanged
    assert updated_address["city"] == "Newtown"
    assert updated_address["zip_code"] == "77002-123"
    assert updated_address["complement"] is None
    assert updated_address["number"] == "789" # Should remain unchanged


def test_update_non_existent_address():
    """
    Test case for updating a non-existent address.
    It should return a 404 status code (Not Found).
    """
    update_data = {
        "street": "Non Existent St",
        "city": "Ghost City",
        "state": "GA",
        "zip_code": "30303",
        "country": "USA"
    }
    response = client.put("/addresses/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"

def test_update_address_invalid_id():
    """
    Test case for updating an address with an invalid ID (e.g., zero or negative).
    It should return a 422 status code (Unprocessable Entity).
    """
    update_data = {
        "street": "Valid St",
        "city": "Valid City",
        "state": "VS",
        "zip_code": "12345",
        "country": "USA"
    }
    response = client.put("/addresses/0", json=update_data)
    assert response.status_code == 422

def test_delete_address():
    """
    Test case for deleting an existing address.
    It should return a 204 status code (No Content).
    """
    # First, create an address to delete
    address_data = {
        "street": "111 Delete Rd",
        "city": "Eraseville",
        "state": "CA",
        "zip_code": "90210",
        "country": "USA"
    }
    create_response = client.post("/addresses/", json=address_data)
    created_id = create_response.json()["id"]

    # Now, delete the address
    response = client.delete(f"/addresses/{created_id}")
    assert response.status_code == 204
    assert not response.content  # No content for 204 response

    # Verify the address is no longer in the "database"
    get_response = client.get(f"/addresses/{created_id}")
    assert get_response.status_code == 404

def test_delete_non_existent_address():
    """
    Test case for deleting a non-existent address.
    It should return a 404 status code (Not Found).
    """
    response = client.delete("/addresses/999")  # ID 999 is unlikely to exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"

def test_delete_address_invalid_id():
    """
    Test case for deleting an address with an invalid ID (e.g., zero or negative).
    It should return a 422 status code (Unprocessable Entity).
    """
    response = client.delete("/addresses/0")  # ID must be > 0
    assert response.status_code == 422
