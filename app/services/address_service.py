from typing import List, Optional
import uuid
from app.repositories.address_repository import address_repo, AddressRepository
from app.schemas.address import Address, AddressCreate, AddressUpdate

class AddressService:
    def __init__(self, repo: AddressRepository = address_repo):
        self.repo = repo

    async def list_addresses(self) -> List[Address]:
        return await self.repo.get_all()

    async def get_address(self, address_id: uuid.UUID) -> Optional[Address]:
        return await self.repo.get_by_id(address_id)

    async def create_address(self, address_in: AddressCreate) -> Address:
        address = Address(id=uuid.uuid4(), **address_in.model_dump())
        return await self.repo.create(address)

    async def update_address(self, address_id: uuid.UUID, address_in: AddressUpdate) -> Optional[Address]:
        existing = await self.repo.get_by_id(address_id)
        if not existing:
            return None
        
        update_data = address_in.model_dump(exclude_unset=True)
        updated_item = existing.model_copy(update=update_data)
        return await self.repo.update(address_id, updated_item)

    async def delete_address(self, address_id: uuid.UUID) -> bool:
        return await self.repo.delete(address_id)

address_service = AddressService()
