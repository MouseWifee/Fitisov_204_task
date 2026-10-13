from app.models.task import Task
from app.repositories.base import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create(self, title: str, description: str, priority: str, due_date: str) -> int:
        task = Task(title=title.strip(), description=description.strip(),
                    priority=priority, due_date=due_date.strip())
        task.validate()
        return self.repository.add(task)

    def edit(self, task: Task) -> None:
        task.validate()
        self.repository.update(task)

    def remove(self, task_id: int) -> None:
        self.repository.delete(task_id)

    def list_tasks(self, search: str = "", status: str = "Все задачи") -> list[Task]:
        tasks = self.repository.get_all()
        query = search.strip().casefold()
        if query:
            tasks = [t for t in tasks if query in t.title.casefold() or query in t.description.casefold()]
        if status == "Активные":
            tasks = [t for t in tasks if not t.completed]
        elif status == "Выполненные":
            tasks = [t for t in tasks if t.completed]
        return tasks

    def statistics(self) -> tuple[int, int, int]:
        tasks = self.repository.get_all()
        completed = sum(t.completed for t in tasks)
        return len(tasks), len(tasks) - completed, completed
