from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from app.schemas.address import Address, AddressCreate, AddressUpdate
from app.services.address_service import address_service

router = APIRouter()

@router.post("/", response_model=Address, status_code=status.HTTP_201_CREATED)
async def create_address(address_in: AddressCreate):
    try:
        return await address_service.create_address(address_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Address])
async def list_addresses():
    return await address_service.list_addresses()

@router.get("/{address_id}", response_model=Address)
async def get_address(address_id: uuid.UUID):
    address = await address_service.get_address(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=Address)
async def update_address(address_id: uuid.UUID, address_in: AddressUpdate):
    address = await address_service.update_address(address_id, address_in)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: uuid.UUID):
    success = await address_service.delete_address(address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return None
