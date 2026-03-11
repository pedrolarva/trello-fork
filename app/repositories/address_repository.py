from app.repositories.base import BaseRepository
from app.schemas.address import Address
import uuid

class AddressRepository(BaseRepository[Address]):
    pass

# Singleton instance for in-memory DB
address_repo = AddressRepository()
