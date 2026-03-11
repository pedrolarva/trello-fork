from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import uuid

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

class AddressUpdate(BaseModel):
    street: Optional[str] = Field(None, min_length=1)
    number: Optional[str] = Field(None, min_length=1)
    complement: Optional[str] = Field(None)
    neighborhood: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, min_length=1)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    zip_code: Optional[str] = Field(None, pattern=r"^\d{5}-\d{3}$")

class Address(AddressBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
