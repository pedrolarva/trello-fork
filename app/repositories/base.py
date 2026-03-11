from typing import Generic, TypeVar, List, Optional
import uuid

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self):
        self._db: List[T] = []

    async def get_all(self) -> List[T]:
        return self._db

    async def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        for item in self._db:
            if getattr(item, "id") == id:
                return item
        return None

    async def create(self, item: T) -> T:
        self._db.append(item)
        return item

    async def update(self, id: uuid.UUID, updated_item: T) -> Optional[T]:
        for i, item in enumerate(self._db):
            if getattr(item, "id") == id:
                self._db[i] = updated_item
                return updated_item
        return None

    async def delete(self, id: uuid.UUID) -> bool:
        for i, item in enumerate(self._db):
            if getattr(item, "id") == id:
                del self._db[i]
                return True
        return False
