from typing import Optional
from task_manager.domain.models import Task, TaskRepository

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_task(self, task_id: str) -> Optional[Task]:
        if not task_id:
            raise ValueError("Task ID cannot be empty")
        return self.repository.get_by_id(task_id)

    def create_task(self, task_id: str, title: str, description: str, status: str = "pending") -> Task:
        if not task_id or not title:
            raise ValueError("Task ID and title are required")
        task = Task(id=task_id, title=title, description=description, status=status)
        self.repository.save(task)
        return task

    def remove_task(self, task_id: str) -> None:
        if not task_id:
            raise ValueError("Task ID cannot be empty")
        self.repository.delete(task_id)
