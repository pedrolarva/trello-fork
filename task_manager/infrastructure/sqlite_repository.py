import sqlite3
from typing import Optional
from task_manager.domain.models import Task, TaskRepository

class SQLiteTaskRepository(TaskRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL
                )
            """)

    def get_by_id(self, task_id: str) -> Optional[Task]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT id, title, description, status FROM tasks WHERE id = ?",
                    (task_id,)
                )
                row = cursor.fetchone()
                if row:
                    return Task(id=row[0], title=row[1], description=row[2], status=row[3])
                return None
        except sqlite3.Error as e:
            # In a real enterprise app, we would use a logger
            raise RuntimeError(f"Database error: {e}")

    def save(self, task: Task) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO tasks (id, title, description, status) VALUES (?, ?, ?, ?)",
                    (task.id, task.title, task.description, task.status)
                )
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")

    def delete(self, task_id: str) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
