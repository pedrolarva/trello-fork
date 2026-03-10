
from typing import List
from fastapi import FastAPI, HTTPException, status, Path
from address_api.schemas import AddressCreate, AddressUpdate, AddressInDB
from address_api.models import (
    create_address_in_db,
    get_address_from_db,
    update_address_in_db,
    delete_address_from_db,
    get_all_addresses_from_db,
)

app = FastAPI(
    title="Address Management API",
    description="API for managing customer addresses with CRUD operations.",
    version="1.0.0",
)

@app.post(
    "/addresses/",
    response_model=AddressInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    tags=["Addresses"],
)
async def create_address(address: AddressCreate) -> AddressInDB:
    """
    Creates a new address in the system.

    - **street**: Street name and number (min: 3, max: 100 characters)
    - **city**: City name (min: 2, max: 50 characters)
    - **state**: State name (min: 2, max: 50 characters)
    - **zip_code**: Zip code (e.g., 12345 or 12345-678)
    - **country**: Country name (min: 2, max: 50 characters)
    - **complement**: Additional address information (optional, max: 100 characters)
    - **number**: House or building number (optional, max: 10 characters)
    """
    try:
        new_address = create_address_in_db(address.model_dump())
        return AddressInDB.model_validate(new_address)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create address: {e}",
        )


@app.get(
    "/addresses/{address_id}",
    response_model=AddressInDB,
    summary="Retrieve an address by ID",
    tags=["Addresses"],
)
async def read_address(
    address_id: int = Path(..., gt=0, description="The ID of the address to retrieve")
) -> AddressInDB:
    """
    Retrieves a single address by its unique ID.

    - **address_id**: The integer ID of the address to retrieve.
    """
    address = get_address_from_db(address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return AddressInDB.model_validate(address)


@app.get(
    "/addresses/",
    response_model=List[AddressInDB],
    summary="Retrieve all addresses",
    tags=["Addresses"],
)
async def read_all_addresses() -> List[AddressInDB]:
    """
    Retrieves a list of all addresses stored in the system.
    """
    addresses = get_all_addresses_from_db()
    return [AddressInDB.model_validate(address) for address in addresses]


@app.put(
    "/addresses/{address_id}",
    response_model=AddressInDB,
    summary="Update an existing address",
    tags=["Addresses"],
)
async def update_address(
    address_id: int = Path(..., gt=0, description="The ID of the address to update"),
    address: AddressUpdate = ...,
) -> AddressInDB:
    """
    Updates an existing address by its ID.

    - **address_id**: The integer ID of the address to update.
    - **address**: The updated address data. Fields not provided will remain unchanged.
    """
    existing_address = get_address_from_db(address_id)
    if not existing_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    try:
        updated_address = update_address_in_db(address_id, address.model_dump(exclude_unset=True))
        if not updated_address:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update address in DB",
            )
        return AddressInDB.model_validate(updated_address)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update address: {e}",
        )


@app.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an address by ID",
    tags=["Addresses"],
)
async def delete_address(
    address_id: int = Path(..., gt=0, description="The ID of the address to delete")
):
    """
    Deletes an address from the system by its ID.

    - **address_id**: The integer ID of the address to delete.
    """
    if not get_address_from_db(address_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    try:
        if not delete_address_from_db(address_id):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete address from DB",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete address: {e}",
        )
