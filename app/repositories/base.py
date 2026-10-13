from abc import ABC, abstractmethod
from app.models.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> int: ...

    @abstractmethod
    def update(self, task: Task) -> None: ...

    @abstractmethod
    def delete(self, task_id: int) -> None: ...

    @abstractmethod
    def get_all(self) -> list[Task]: ...
