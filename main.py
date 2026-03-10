
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

app = FastAPI(title="Address API")

class AddressBase(BaseModel):
    street: str = Field(..., min_length=1, json_schema_extra={"example": "Rua da Consolação"})
    number: str = Field(..., min_length=1, json_schema_extra={"example": "123"})
    complement: Optional[str] = Field(None, json_schema_extra={"example": "Apto 101"})
    neighborhood: str = Field(..., min_length=1, json_schema_extra={"example": "Centro"})
    city: str = Field(..., min_length=1, json_schema_extra={"example": "São Paulo"})
    state: str = Field(..., min_length=2, max_length=2, json_schema_extra={"example": "SP"})
    zip_code: str = Field(..., pattern=r"^\d{5}-\d{3}$", json_schema_extra={"example": "01301-100"})

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    street: Optional[str] = Field(None, min_length=1, json_schema_extra={"example": "Rua da Consolação"})
    number: Optional[str] = Field(None, min_length=1, json_schema_extra={"example": "123"})
    neighborhood: Optional[str] = Field(None, min_length=1, json_schema_extra={"example": "Centro"})
    city: Optional[str] = Field(None, min_length=1, json_schema_extra={"example": "São Paulo"})
    state: Optional[str] = Field(None, min_length=2, max_length=2, json_schema_extra={"example": "SP"})
    zip_code: Optional[str] = Field(None, pattern=r"^\d{5}-\d{3}$", json_schema_extra={"example": "01301-100"})

class AddressInDB(AddressBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    model_config = {'from_attributes': True}

# In-memory database
db: List[AddressInDB] = []

@app.post("/addresses/", response_model=AddressInDB, status_code=status.HTTP_201_CREATED)
async def create_address(address: AddressCreate):
    try:
        address_in_db = AddressInDB(**address.model_dump())
        db.append(address_in_db)
        return address_in_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create address: {e}"
        )

@app.get("/addresses/", response_model=List[AddressInDB])
async def read_addresses():
    return db

@app.get("/addresses/{address_id}", response_model=AddressInDB)
async def read_address(address_id: uuid.UUID):
    for address in db:
        if address.id == address_id:
            return address
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

@app.put("/addresses/{address_id}", response_model=AddressInDB)
async def update_address(address_id: uuid.UUID, address: AddressUpdate):
    for index, existing_address in enumerate(db):
        if existing_address.id == address_id:
            try:
                updated_data = address.model_dump(exclude_unset=True)
                updated_address = existing_address.model_copy(update=updated_data)
                db[index] = updated_address
                return updated_address
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to update address: {e}"
                )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

@app.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: uuid.UUID):
    for index, address in enumerate(db):
        if address.id == address_id:
            del db[index]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

