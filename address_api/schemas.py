
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class AddressBase(BaseModel):
    street: str = Field(..., min_length=3, max_length=100, description="Street name and number")
    city: str = Field(..., min_length=2, max_length=50, description="City name")
    state: str = Field(..., min_length=2, max_length=50, description="State name")
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{3})?$", description="Zip code (e.g., 12345 or 12345-678)")
    country: str = Field(..., min_length=2, max_length=50, description="Country name")
    complement: Optional[str] = Field(None, max_length=100, description="Additional address information")
    number: Optional[str] = Field(None, max_length=10, description="House or building number")

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    street: Optional[str] = Field(None, min_length=3, max_length=100, description="Street name and number")
    city: Optional[str] = Field(None, min_length=2, max_length=50, description="City name")
    state: Optional[str] = Field(None, min_length=2, max_length=50, description="State name")
    zip_code: Optional[str] = Field(None, pattern=r"^\d{5}(-\d{3})?$", description="Zip code (e.g., 12345 or 12345-678)")
    country: Optional[str] = Field(None, min_length=2, max_length=50, description="Country name")

class AddressInDB(AddressBase):
    id: int = Field(..., ge=1, description="Unique identifier for the address")

    class Config:
        from_attributes = True

