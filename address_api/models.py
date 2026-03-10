
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# This would typically be an ORM model (e.g., SQLAlchemy, Tortoise-ORM)
# For this exercise, we'll use a Pydantic model to simulate the data structure
# that would be stored in a database.

class Address(BaseModel):
    id: int = Field(..., ge=1, description="Unique identifier for the address")
    street: str = Field(..., min_length=3, max_length=100, description="Street name and number")
    city: str = Field(..., min_length=2, max_length=50, description="City name")
    state: str = Field(..., min_length=2, max_length=50, description="State name")
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{3})?$", description="Zip code (e.g., 12345 or 12345-678)")
    country: str = Field(..., min_length=2, max_length=50, description="Country name")
    complement: Optional[str] = Field(None, max_length=100, description="Additional address information")
    number: Optional[str] = Field(None, max_length=10, description="House or building number")

    class Config:
        from_attributes = True

# In-memory database for demonstration purposes
# In a real application, this would be replaced with a proper database connection
# and ORM operations.
db: Dict[int, Address] = {}
next_id: int = 1

def get_next_id() -> int:
    """Generates a unique ID for new addresses."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

def create_address_in_db(address_data: dict) -> Address:
    """
    Simulates saving a new address to the database.
    """
    global db
    new_id = get_next_id()
    address = Address(id=new_id, **address_data)
    db[new_id] = address
    return address

def get_address_from_db(address_id: int) -> Optional[Address]:
    """
    Simulates retrieving an address from the database by its ID.
    """
    return db.get(address_id)

def update_address_in_db(address_id: int, update_data: Dict) -> Optional[Address]:
    """
    Simulates updating an existing address in the database.
    """
    global db
    if address_id in db:
        current_address = db[address_id]
        updated_fields = current_address.model_dump()
        for key, value in update_data.items():
            if value is not None:
                updated_fields[key] = value
        updated_address = Address(**updated_fields)
        db[address_id] = updated_address
        return updated_address
    return None

def delete_address_from_db(address_id: int) -> bool:
    """
    Simulates deleting an address from the database.
    """
    global db
    if address_id in db:
        del db[address_id]
        return True
    return False

def get_all_addresses_from_db() -> List[Address]:
    """
    Simulates retrieving all addresses from the database.
    """
    return list(db.values())
