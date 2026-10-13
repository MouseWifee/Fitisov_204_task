import sqlite3
from pathlib import Path
from app.models.task import Task
from app.repositories.base import TaskRepository


class SQLiteTaskRepository(TaskRepository):
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    priority TEXT NOT NULL DEFAULT 'Средний',
                    due_date TEXT NOT NULL DEFAULT '',
                    completed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
                )
            """)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, task: Task) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks(title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, ?)",
                (task.title, task.description, task.priority, task.due_date, int(task.completed)),
            )
            return int(cur.lastrowid)

    def update(self, task: Task) -> None:
        if task.id is None:
            raise ValueError("Нельзя обновить задачу без ID.")
        with self._connect() as conn:
            conn.execute(
                "UPDATE tasks SET title=?, description=?, priority=?, due_date=?, completed=? WHERE id=?",
                (task.title, task.description, task.priority, task.due_date, int(task.completed), task.id),
            )

    def delete(self, task_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))

    def get_all(self) -> list[Task]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM tasks ORDER BY completed, id DESC").fetchall()
        return [Task(id=r['id'], title=r['title'], description=r['description'],
                     priority=r['priority'], due_date=r['due_date'],
                     completed=bool(r['completed']), created_at=r['created_at']) for r in rows]
