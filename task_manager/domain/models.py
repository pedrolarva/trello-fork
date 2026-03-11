from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod

@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str

class TaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        pass
