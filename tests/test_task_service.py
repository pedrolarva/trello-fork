import pytest
import os
from task_manager.infrastructure.sqlite_repository import SQLiteTaskRepository
from task_manager.application.task_service import TaskService
from task_manager.domain.models import Task

@pytest.fixture
def test_db():
    db_path = "test_factory.db"
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def task_service(test_db):
    repo = SQLiteTaskRepository(test_db)
    return TaskService(repo)

def test_create_and_get_task(task_service):
    task_id = "test-id-123"
    task_service.create_task(task_id, "Test Task", "Description")
    
    task = task_service.get_task(task_id)
    assert task is not None
    assert task.id == task_id
    assert task.title == "Test Task"

def test_get_non_existent_task(task_service):
    task = task_service.get_task("non-existent")
    assert task is None

def test_create_task_invalid_input(task_service):
    with pytest.raises(ValueError):
        task_service.create_task("", "", "")

def test_delete_task(task_service):
    task_id = "delete-me"
    task_service.create_task(task_id, "To be deleted", "")
    task_service.remove_task(task_id)
    
    task = task_service.get_task(task_id)
    assert task is None
